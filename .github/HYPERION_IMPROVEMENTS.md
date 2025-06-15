# Hyperion.NG Download Reliability Improvements

## Overview
This document outlines the improvements made to the Hyperion.NG add-on download mechanism to increase reliability and reduce brittleness.

## Problems Addressed

### 1. Brittle Architecture Mapping
**Before**: Hard-coded architecture mapping in Dockerfile that didn't match actual Hyperion release naming
- `armhf` → `armv7` (incorrect, caused 404 errors)

**After**: Correct architecture mapping based on actual GitHub releases
- `amd64` → `x86_64`
- `armhf` → `armv7l` (fixed)
- `aarch64` → `arm64`

### 2. Unreliable Release Detection
**Before**: Used `git ls-remote` with basic string parsing that could fail with complex version schemes

**After**: Multi-layered approach with fallbacks:
1. GitHub API (primary) - Most reliable, gets structured release data
2. Git ls-remote (fallback) - Improved parsing with version sorting
3. Proper error handling and validation

### 3. Poor Download Handling
**Before**: Single attempt wget with minimal error reporting

**After**: Robust download system:
- Multi-attempt downloads (3 retries with exponential backoff)
- Support for both curl and wget
- Progress reporting
- Comprehensive error logging
- Download verification (file size, gzip integrity)

### 4. No Asset Validation
**Before**: No verification that required binaries exist before attempting build

**After**: Pre-validation of release assets:
- Checks all required architectures are available
- Warns about missing assets
- Prevents builds from failing due to missing releases

## Implementation Details

### Files Modified/Created

1. **`.github/scripts/update-hyperion-version.sh`** - Enhanced version detection
   - GitHub API integration with fallback
   - Proper JSON parsing with jq
   - Asset validation before version update
   - Atomic file updates with temp files

2. **`.github/scripts/download-hyperion.sh`** - New robust download script
   - Comprehensive error handling and logging
   - Multi-attempt downloads with different tools
   - File verification and integrity checks
   - Detailed progress reporting

3. **`addon-hyperion-ng/Dockerfile`** - Simplified and more reliable
   - Uses dedicated download script
   - Better error reporting
   - Installation verification
   - Added curl dependency for better download reliability

### Key Features

#### Error Handling
- All scripts use `set -euo pipefail` for strict error handling
- Comprehensive error messages with context
- Proper cleanup of temporary files
- Non-zero exit codes on failure

#### Download Reliability
- Multiple download attempts with backoff
- Support for both curl and wget
- Connection and timeout handling
- Progress reporting for user feedback

#### Validation
- Release existence verification via GitHub API
- Asset availability checking
- File integrity validation (gzip test)
- Installation verification (binary presence)

#### Logging
- Timestamped log messages
- Detailed error reporting
- Progress indicators
- Debug information for troubleshooting

## Testing

### Architecture Mapping Verification
```bash
# All three architectures verified available for v2.1.1
curl -I "https://github.com/hyperion-project/hyperion.ng/releases/download/2.1.1/Hyperion-2.1.1-Linux-x86_64.tar.gz"  # ✓
curl -I "https://github.com/hyperion-project/hyperion.ng/releases/download/2.1.1/Hyperion-2.1.1-Linux-armv7l.tar.gz"  # ✓
curl -I "https://github.com/hyperion-project/hyperion.ng/releases/download/2.1.1/Hyperion-2.1.1-Linux-arm64.tar.gz"   # ✓
```

### API Integration
```bash
# GitHub API returns current version: 2.1.1
curl -s "https://api.github.com/repos/hyperion-project/hyperion.ng/releases/latest" | jq -r '.tag_name'
```

## Benefits

1. **Reduced Build Failures**: Better error handling and retries reduce transient failures
2. **Faster Debugging**: Detailed logging helps identify issues quickly
3. **Future-Proof**: API-based approach adapts to new releases automatically
4. **Maintainable**: Modular scripts are easier to update and test
5. **Robust**: Multiple fallback mechanisms prevent single points of failure

## Migration Notes

- No changes required to existing configuration files
- Backward compatible with existing workflows
- Enhanced logging provides better visibility into build process
- Failed builds now provide more actionable error messages

## Future Improvements

1. **Checksum Verification**: Add SHA256 hash verification if Hyperion project provides checksums
2. **Mirror Support**: Add support for alternative download mirrors
3. **Caching**: Implement download caching to reduce GitHub API usage
4. **Notification**: Add webhook support for build failure notifications