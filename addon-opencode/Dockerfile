# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:latest
FROM $BUILD_FROM

# Execute during the build of the image
ARG OPENCODE_VERSION
ARG BUILD_ARCH
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -q -y \
    && apt-get install -q -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    jq \
    ripgrep \
    nodejs \
    npm \
    python3 \
    python3-pip \
    tar \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN set -euo pipefail; \
    case "${BUILD_ARCH}" in \
      aarch64) target="linux-arm64" ;; \
      amd64) target="linux-x64-baseline" ;; \
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
