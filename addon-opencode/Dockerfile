# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base:stable
FROM $BUILD_FROM

# Execute during the build of the image
ARG OPENCODE_VERSION
ARG BUILD_ARCH
ARG HA_CLI_VERSION="4.45.0"

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base
RUN \
    export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    \
    && apt-get install -q -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    jq \
    mariadb-client \
    mosquitto-clients \
    ripgrep \
    nodejs \
    nano \
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

# Install HA CLI
RUN curl -L -s -o /usr/bin/ha \
    "https://github.com/home-assistant/cli/releases/download/${HA_CLI_VERSION}/ha_${BUILD_ARCH}" \
    && chmod a+x /usr/bin/ha

# Copy root filesystem
COPY rootfs /

# Health check
HEALTHCHECK --start-period=10m \
    CMD curl --fail http://127.0.0.1:4096 || exit 1


# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Jonathan Bradshaw <jb@nrgup.net>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Community Apps" \
    org.opencontainers.image.authors="Jonathan Bradshaw <jb@nrgup.net>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
