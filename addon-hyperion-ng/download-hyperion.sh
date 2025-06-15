#!/bin/bash
set -euo pipefail

#
# Robust Hyperion.NG Download Script
# Handles architecture mapping, retries, and validation
#

usage() {
    echo "Usage: $0 <version> <build_arch> <output_dir>"
    echo "  version:    Hyperion version (e.g., 2.1.1)"
    echo "  build_arch: Home Assistant architecture (amd64, armhf, aarch64)"
    echo "  output_dir: Directory to extract to"
    exit 1
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Architecture mapping function
map_architecture() {
    local build_arch="$1"
    case "$build_arch" in
        amd64) echo "x86_64" ;;
        armhf) echo "armv7l" ;;
        aarch64) echo "arm64" ;;
        *) 
            log "ERROR: Unsupported architecture: $build_arch"
            log "Supported: amd64, armhf, aarch64"
            exit 1
            ;;
    esac
}

# Validate inputs
validate_inputs() {
    local version="$1"
    local build_arch="$2"
    local output_dir="$3"
    
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$ ]]; then
        log "ERROR: Invalid version format: $version"
        log "Expected format: X.Y.Z or X.Y.Z-suffix"
        exit 1
    fi
    
    if [[ ! -d "$output_dir" ]]; then
        log "ERROR: Output directory does not exist: $output_dir"
        exit 1
    fi
    
    if [[ ! -w "$output_dir" ]]; then
        log "ERROR: Output directory is not writable: $output_dir"
        exit 1
    fi
}

# Download with retries and progress
download_with_retries() {
    local url="$1"
    local output_file="$2"
    local max_attempts=3
    local timeout=60
    
    log "Downloading: $url"
    
    for attempt in $(seq 1 $max_attempts); do
        log "Attempt $attempt/$max_attempts..."
        
        if command -v curl >/dev/null 2>&1; then
            # Prefer curl if available
            if curl -L --fail --connect-timeout 30 --max-time $timeout \
                    --progress-bar --output "$output_file" "$url"; then
                log "Download successful (curl)"
                return 0
            fi
        elif command -v wget >/dev/null 2>&1; then
            # Fallback to wget
            if wget --timeout=$timeout --tries=1 --progress=bar:force \
                    -O "$output_file" "$url"; then
                log "Download successful (wget)"
                return 0
            fi
        else
            log "ERROR: Neither curl nor wget is available"
            exit 1
        fi
        
        log "Download attempt $attempt failed"
        rm -f "$output_file"
        
        if [[ $attempt -lt $max_attempts ]]; then
            local delay=$((attempt * 5))
            log "Waiting ${delay}s before retry..."
            sleep $delay
        fi
    done
    
    log "ERROR: Download failed after $max_attempts attempts"
    return 1
}

# Verify downloaded file
verify_download() {
    local file="$1"
    local expected_size_min=10485760  # 10MB minimum
    
    if [[ ! -f "$file" ]]; then
        log "ERROR: Downloaded file not found: $file"
        return 1
    fi
    
    local file_size
    file_size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo "0")
    
    if [[ $file_size -lt $expected_size_min ]]; then
        log "ERROR: Downloaded file too small: ${file_size} bytes (expected > ${expected_size_min})"
        log "File might be corrupted or incomplete"
        return 1
    fi
    
    # Test if it's a valid gzip file
    if ! gzip -t "$file" 2>/dev/null; then
        log "ERROR: Downloaded file is not a valid gzip archive"
        log "File info:"
        ls -la "$file" || true
        log "File header:"
        head -c 100 "$file" | xxd || true
        return 1
    fi
    
    log "Download verification passed (${file_size} bytes)"
    return 0
}

# Extract archive
extract_archive() {
    local archive="$1"
    local output_dir="$2"
    
    log "Extracting to: $output_dir"
    
    if tar -xzf "$archive" -C "$output_dir"; then
        log "Extraction successful"
        
        # List installed files for verification
        if find "$output_dir" -name "*hyperion*" -type f -executable 2>/dev/null | head -5; then
            log "Hyperion binaries found:"
            find "$output_dir" -name "*hyperion*" -type f -executable -exec ls -la {} \; | head -5
        fi
        
        return 0
    else
        log "ERROR: Failed to extract archive"
        return 1
    fi
}

# Main function
main() {
    if [[ $# -ne 3 ]]; then
        usage
    fi
    
    local version="$1"
    local build_arch="$2"
    local output_dir="$3"
    
    log "Starting Hyperion download process"
    log "Version: $version"
    log "Build Architecture: $build_arch"
    log "Output Directory: $output_dir"
    
    # Validate inputs
    validate_inputs "$version" "$build_arch" "$output_dir"
    
    # Map architecture
    local hyperion_arch
    hyperion_arch=$(map_architecture "$build_arch")
    log "Hyperion Architecture: $hyperion_arch"
    
    # Construct download URL
    local base_url="https://github.com/hyperion-project/hyperion.ng/releases/download"
    local filename="Hyperion-${version}-Linux-${hyperion_arch}.tar.gz"
    local download_url="${base_url}/${version}/${filename}"
    
    # Create temporary file
    local temp_file
    temp_file=$(mktemp)
    trap "rm -f '$temp_file'" EXIT
    
    # Download
    if ! download_with_retries "$download_url" "$temp_file"; then
        log "ERROR: Failed to download Hyperion"
        exit 1
    fi
    
    # Verify
    if ! verify_download "$temp_file"; then
        log "ERROR: Download verification failed"
        exit 1
    fi
    
    # Extract
    if ! extract_archive "$temp_file" "$output_dir"; then
        log "ERROR: Failed to extract Hyperion"
        exit 1
    fi
    
    log "Hyperion $version installation completed successfully"
}

# Run main function
main "$@"