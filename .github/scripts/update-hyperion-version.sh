#!/bin/bash
set -euo pipefail

# Default to current directory if GITHUB_WORKSPACE not set
BASE=${GITHUB_WORKSPACE:-$(pwd)}/addon-hyperion-ng
FILE="${BASE}/config.yaml"

# Check if config.yaml exists
if [[ ! -f "$FILE" ]]; then
    echo "ERROR: config.yaml not found at: $FILE" >&2
    echo "Please run from repository root or set GITHUB_WORKSPACE" >&2
    exit 1
fi

# Read the one expected top-level YAML version line.
version_line_count=$(grep -cE '^version: "[^"]+"$' "$FILE" || true)
if [[ "$version_line_count" -ne 1 ]]; then
    echo "ERROR: Expected exactly one top-level version line in: $FILE" >&2
    exit 1
fi

version_line=$(grep -E '^version: "[^"]+"$' "$FILE")
CURRENT="${version_line#version: \"}"
CURRENT="${CURRENT%\"}"
echo "Current version: ${CURRENT}"

# Only write to GITHUB_ENV if it exists (GitHub Actions environment)
if [[ -n "${GITHUB_ENV:-}" ]]; then
    echo "VERSION=${CURRENT}" >> "$GITHUB_ENV"
else
    echo "Local mode: GITHUB_ENV not set, skipping environment export"
    export VERSION="$CURRENT"
fi

# Function to get latest release using GitHub API with fallback
get_latest_release() {
    local api_url="https://api.github.com/repos/hyperion-project/hyperion.ng/releases/latest"
    local git_repo="https://github.com/hyperion-project/hyperion.ng.git"
    
    echo "Fetching latest release from GitHub API..." >&2
    
    # Try GitHub API first (more reliable)
    if command -v curl >/dev/null 2>&1; then
        local release_json
        if release_json=$(curl -s --fail --connect-timeout 10 --max-time 30 "$api_url" 2>/dev/null); then
            local tag_name
            tag_name=$(echo "$release_json" | jq -r '.tag_name // empty')
            if [[ -n "$tag_name" && "$tag_name" != "null" ]]; then
                echo "Found release via API: ${tag_name}" >&2
                echo "$tag_name"
                return 0
            fi
        fi
    fi
    
    echo "API failed, falling back to git ls-remote..." >&2
    
    # Fallback to git ls-remote with improved parsing
    local release
    if release=$(git ls-remote --tags --sort='-version:refname' "$git_repo" 2>/dev/null | \
                 grep -E 'refs/tags/[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$' | \
                 head -n1 | \
                 sed 's/.*refs\/tags\///' 2>/dev/null); then
        if [[ -n "$release" ]]; then
            echo "Found release via git: ${release}" >&2
            echo "$release"
            return 0
        fi
    fi
    
    echo "ERROR: Failed to fetch latest release" >&2
    return 1
}

# Function to validate release exists and has required assets
validate_release() {
    local release="$1"
    local required_archs=("amd64" "arm64")
    local base_url="https://github.com/hyperion-project/hyperion.ng/releases/download/${release}"
    
    echo "Validating release ${release} has required assets..." >&2
    
    if ! command -v curl >/dev/null 2>&1; then
        echo "ERROR: curl is required to validate release assets" >&2
        return 1
    fi

    for arch in "${required_archs[@]}"; do
        local asset_url="${base_url}/Hyperion-${release}-Linux-${arch}.tar.gz"
        echo "Checking: ${asset_url}" >&2
        
        if ! curl --silent --show-error --location --head --fail \
            --connect-timeout 10 --max-time 15 "$asset_url" >/dev/null; then
            echo "ERROR: Required asset not found for ${arch}: ${asset_url}" >&2
            return 1
        fi

        echo "Asset found for ${arch}" >&2
    done
}

# Get latest release
if ! RELEASE=$(get_latest_release); then
    echo "ERROR: Could not determine latest release" >&2
    exit 1
fi

# Export release version
if [[ -n "${GITHUB_ENV:-}" ]]; then
    echo "RELEASE=${RELEASE}" >> "$GITHUB_ENV"
else
    echo "Local mode: Would set RELEASE=${RELEASE}"
    export RELEASE="$RELEASE"
fi

# Validate the release has the required assets
validate_release "$RELEASE"

# Update version if changed
if [[ "$CURRENT" != "$RELEASE" ]]; then
    echo "Updating version from ${CURRENT} to ${RELEASE}"
    
    # In local mode, ask for confirmation before updating
    if [[ -z "${GITHUB_ENV:-}" ]]; then
        echo "Local mode: Would update config.yaml from ${CURRENT} to ${RELEASE}"
        read -p "Continue with update? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Update cancelled by user"
            exit 0
        fi
    fi
    
    # Replace the validated top-level version line in an atomic update.
    temp_file=$(mktemp "${FILE}.tmp.XXXXXX")
    
    if while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == "$version_line" ]]; then
            printf 'version: "%s"\n' "$RELEASE"
        else
            printf '%s\n' "$line"
        fi
    done < "$FILE" > "$temp_file"; then
        if mv "$temp_file" "$FILE"; then
            echo "Version updated successfully"
        else
            rm -f "$temp_file"
            echo "ERROR: Failed to update version in config.yaml" >&2
            exit 1
        fi
    else
        rm -f "$temp_file"
        echo "ERROR: Failed to update version in config.yaml" >&2
        exit 1
    fi
else
    echo "Version unchanged: ${CURRENT}"
fi
