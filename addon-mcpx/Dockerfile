# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
ARG MCPX_REF=e4a70047221fa015973d78858b7bdfd7ca321b32

FROM node:22.22.0-alpine3.22 AS upstream-source
ARG MCPX_REF

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

RUN apk add --no-cache ca-certificates curl patch tar

WORKDIR /src
RUN curl -fsSL "https://github.com/TheLunarCompany/lunar/archive/${MCPX_REF}.tar.gz" \
    | tar -xz --strip-components=1

COPY patches/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch /tmp/
RUN patch --batch --forward -p1 < /tmp/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch

FROM node:22.22.0-alpine3.22 AS base

ENV HOME=/lunar

WORKDIR ${HOME}

COPY --from=upstream-source /src/mcpx/packages ./packages
COPY --from=upstream-source /src/mcpx/package.json ./package.json
COPY --from=upstream-source /src/mcpx/package-lock.json ./package-lock.json
COPY --from=upstream-source /src/mcpx/scripts/generate-config.sh ./scripts/generate-config.sh
COPY --from=upstream-source /src/mcpx/deps.json ./deps.json
COPY --from=upstream-source /src/mcpx/build-deps.cjs ./build-deps.cjs
COPY --from=upstream-source /src/mcpx/.version ./.version
RUN VERSION_VALUE=$(tr -d '\n' < .version) \
    && echo "${VERSION_VALUE}" > /tmp/version.env

RUN npm run build:deps && npm install
RUN npm run install:mcpx-server && npm run build:mcpx-server

WORKDIR ${HOME}/packages/ui
COPY --from=upstream-source /src/mcpx/scripts/generate-config.sh generate-config.sh

RUN ARCH=$(uname -m) \
    && if [ "${ARCH}" = "aarch64" ] || [ "${ARCH}" = "arm64" ]; then \
        npm install @rollup/rollup-linux-arm64-musl --save-dev --no-audit --no-fund 2>/dev/null || true; \
    else \
        npm install @rollup/rollup-linux-x64-musl --save-dev --no-audit --no-fund 2>/dev/null || true; \
    fi

WORKDIR ${HOME}
RUN npm run install:ui && npm run build:ui

FROM ${BUILD_FROM}
ARG MCPX_REF

ENV UI_PORT=5173 \
    UI_URL=http://127.0.0.1:5173 \
    LUNAR_USER=lunar \
    LUNAR_USER_UID=1002 \
    LUNAR_USER_GID=1002 \
    LUNAR_USER_GROUP=lunar:lunar \
    HOME=/lunar \
    MCPX_SERVER_PORT=9000 \
    BUILD_SCOPE=all \
    LUNAR_TELEMETRY=false \
    LUNAR_CONSUMER_NAME=mcpx-home-assistant \
    LUNAR_URL= \
    LUNAR_API_KEY= \
    SERVE_METRICS_PORT=3000 \
    MCPX_PORT=9000 \
    ENABLE_CONTROL_PLANE_STREAMING=true \
    ENABLE_CONTROL_PLANE_REST=true \
    MCPX_SERVER_URL=http://127.0.0.1:9000 \
    MITM_PROXY_LISTEN_PORT=8081 \
    MITM_PROXY_LISTEN_HOST=0.0.0.0 \
    VERSION= \
    INSTANCE_ID= \
    INTERCEPTION_USER=lunar_interception \
    INTERCEPTION_USER_UID=1001 \
    INTERCEPTION_USER_GID=1001 \
    SHARED_GROUP_NAME=lunar_group \
    SHARED_GROUP_GID=1050 \
    LOKI_HOST= \
    LOKI_USER= \
    LOKI_PASSWORD= \
    MITM_PROXY_CONF_DIR=/home/lunar_interception/.proxy \
    GITHUB_OAUTH_CLIENT_ID= \
    PYTHONWARNINGS=ignore::UserWarning \
    UV_CACHE_DIR=/lunar/.cache/uv \
    UV_DATA_DIR=/lunar/.local/share/uv \
    UV_TOOL_DIR=/lunar/.local/bin \
    UV_PYTHON_INSTALL_DIR=/lunar/.local/share/uv/python \
    NPM_CONFIG_USERCONFIG=/lunar/.npm/ \
    NPM_CONFIG_CACHE=/lunar/.npm/ \
    DOCKER_CONFIG=/lunar/.docker \
    PIP_NO_CACHE_DIR=1 \
    PIP_USE_PEP517=1 \
    CARGO_HOME=/tmp/cargo \
    RUSTUP_HOME=/tmp/rustup \
    PATH=/tmp/cargo/bin:/lunar/.local/bin:${PATH} \
    DIND_ENABLED=false \
    INTERCEPTION_ENABLED=false \
    VITE_MCPX_SERVER_URL= \
    VITE_MCPX_SERVER_PORT=9000 \
    VITE_WS_URL= \
    VITE_ENABLE_LOGIN=false

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR ${HOME}

RUN apk add --no-cache \
    bash \
    ca-certificates \
    cargo \
    curl \
    docker-cli \
    gcc \
    ipset \
    iptables \
    jq \
    libcap \
    libcap-utils \
    libexpat \
    linux-headers \
    musl-dev \
    nodejs \
    npm \
    py3-pip \
    python3 \
    python3-dev \
    rust \
    su-exec \
    uv \
    && pip3 install --no-cache-dir --break-system-packages 'setuptools<81' supervisor==4.2.5 \
    && npm install -g serve --cache /tmp/empty-cache \
    && rm -rf /tmp/empty-cache

RUN addgroup -g ${LUNAR_USER_GID} -S ${LUNAR_USER} \
    && adduser -u ${LUNAR_USER_UID} -S -D -G ${LUNAR_USER} -h ${HOME} -s /sbin/nologin ${LUNAR_USER} \
    && addgroup -g ${INTERCEPTION_USER_GID} -S ${INTERCEPTION_USER} \
    && adduser -u ${INTERCEPTION_USER_UID} -S -D -G ${INTERCEPTION_USER} -h ${HOME}/${INTERCEPTION_USER} -s /sbin/nologin ${INTERCEPTION_USER} \
    && addgroup -g ${SHARED_GROUP_GID} -S ${SHARED_GROUP_NAME} \
    && addgroup ${LUNAR_USER} ${SHARED_GROUP_NAME} \
    && addgroup ${INTERCEPTION_USER} ${SHARED_GROUP_NAME}

RUN mkdir -p ${UV_CACHE_DIR} ${UV_DATA_DIR} ${UV_TOOL_DIR} ${UV_PYTHON_INSTALL_DIR} ${NPM_CONFIG_USERCONFIG} ${MITM_PROXY_CONF_DIR} ${DOCKER_CONFIG} \
    && mkdir -p /var/log/${LUNAR_USER} ${HOME} ${HOME}/${INTERCEPTION_USER} \
    && chown -R root:${SHARED_GROUP_NAME} /var/log/${LUNAR_USER} || true \
    && chown -R ${LUNAR_USER}:${LUNAR_USER} ${HOME} \
    && chown -R ${INTERCEPTION_USER}:${INTERCEPTION_USER} ${HOME}/${INTERCEPTION_USER} \
    && chmod -R 755 ${NPM_CONFIG_USERCONFIG}

COPY --from=base /tmp/version.env /tmp/version.env
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/shared-model/dist packages/shared-model/dist
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/shared-model/package.json packages/shared-model/package.json
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/toolkit-core/dist packages/toolkit-core/dist
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/toolkit-core/package.json packages/toolkit-core/package.json
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/webapp-protocol/dist packages/webapp-protocol/dist
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/webapp-protocol/package.json packages/webapp-protocol/package.json
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/toolkit-ui/dist packages/toolkit-ui/dist
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/toolkit-ui/package.json packages/toolkit-ui/package.json
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/mcpx-server/dist/src packages/mcpx-server/dist
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/mcpx-server/package.json packages/mcpx-server/package.json
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/node_modules node_modules
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/scripts/generate-config.sh /usr/local/bin/generate-config.sh
COPY --from=base --chown=${LUNAR_USER}:${SHARED_GROUP_NAME} ${HOME}/packages/ui/dist packages/ui
COPY rootfs /

RUN chmod +x /etc/services.d/mcpx/run \
    && chmod +x /etc/services.d/mcpx/finish

EXPOSE 9000 5173 3000

HEALTHCHECK --start-period=2m \
    CMD curl --fail http://127.0.0.1:9000/healthcheck || exit 1

# Build arguments
ARG BUILD_ARCH=amd64
ARG BUILD_DATE
ARG BUILD_DESCRIPTION="MCPX gateway and control plane add-on."
ARG BUILD_NAME="MCPX Server"
ARG BUILD_REF
ARG BUILD_REPOSITORY="bradsjm/hassio-addons"
ARG BUILD_VERSION=0.2.0

# Labels
LABEL \
    io.hass.name="MCPX Server" \
    io.hass.description="MCPX gateway and control plane add-on." \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="app" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Jonathan Bradshaw <jb@nrgup.net>" \
    org.opencontainers.image.title="MCPX Server" \
    org.opencontainers.image.description="MCPX gateway and control plane add-on." \
    org.opencontainers.image.vendor="Home Assistant Community Apps" \
    org.opencontainers.image.authors="Jonathan Bradshaw <jb@nrgup.net>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/addon-mcpx/DOCS.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION} \
    org.opencontainers.image.ref.name="${MCPX_REF}" \
    dev.lunar.mcpx.ref="${MCPX_REF}"
