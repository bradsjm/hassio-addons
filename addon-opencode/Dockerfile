# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base
FROM $BUILD_FROM

# Execute during the build of the image
ARG OPENCODE_VERSION
ARG BUILD_ARCH
RUN apk add --no-cache bash curl tar nodejs npm python3 py3-pip py3-uv libc6-compat gcompat

RUN set -euo pipefail; \
    case "${BUILD_ARCH}" in \
      aarch64) target="linux-arm64-musl" ;; \
      amd64) target="linux-x64-baseline-musl" ;; \
      *) echo "Unsupported BUILD_ARCH: ${BUILD_ARCH}"; exit 1 ;; \
    esac; \
    if [ -n "${OPENCODE_VERSION}" ]; then \
      version="${OPENCODE_VERSION#v}"; \
      url="https://github.com/anomalyco/opencode/releases/download/v${version}/opencode-${target}.tar.gz"; \
    else \
      url="https://github.com/anomalyco/opencode/releases/latest/download/opencode-${target}.tar.gz"; \
    fi; \
    mkdir -p /tmp/opencode; \
    curl -fsSL -o /tmp/opencode/opencode.tar.gz "${url}"; \
    tar -xzf /tmp/opencode/opencode.tar.gz -C /tmp/opencode; \
    install -m 0755 /tmp/opencode/opencode /usr/bin/opencode; \
    rm -rf /tmp/opencode

# Copy root filesystem
COPY rootfs /
