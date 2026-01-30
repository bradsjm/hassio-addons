# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base
FROM $BUILD_FROM

# Execute during the build of the image
ARG OPENCODE_VERSION
RUN apk add --no-cache bash curl tar nodejs npm python3 py3-pip py3-uv
RUN if [ -n "${OPENCODE_VERSION}" ]; then \
        curl -fsSL https://opencode.ai/install | VERSION="${OPENCODE_VERSION}" bash; \
    else \
        curl -fsSL https://opencode.ai/install | bash; \
    fi
RUN install -m 0755 /root/.opencode/bin/opencode /usr/bin/opencode \
    && rm -rf /root/.opencode

# Copy root filesystem
COPY rootfs /
