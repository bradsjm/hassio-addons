# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base
FROM $BUILD_FROM

# Execute during the build of the image
ARG OPENCODE_VERSION
ARG BUILD_ARCH
ARG GLIBC_VERSION=2.39-r0
RUN apk add --no-cache bash ca-certificates curl tar nodejs npm python3 py3-pip py3-uv libc6-compat gcompat

RUN set -euo pipefail; \
    curl -fsSL -o /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub; \
    curl -fsSL -o /tmp/glibc.apk "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-${GLIBC_VERSION}.apk"; \
    apk add --no-cache /tmp/glibc.apk; \
    rm -f /tmp/glibc.apk

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
