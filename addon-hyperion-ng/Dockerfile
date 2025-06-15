ARG BUILD_FROM

FROM ${BUILD_FROM}
ARG DOWNLOAD_URL
ARG BUILD_VERSION
ARG BUILD_ARCH

ENV LANG C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
		libqt5widgets5 \
		libqt5serialport5 \
		libqt5sql5-sqlite \
		libqt5x11extras5 \
		libavahi-core7 \
		libavahi-compat-libdnssd1 \
		libusb-1.0-0 \
		libjpeg-dev \
		libssl1.1 \
		zlib1g \
		libcec6 \
		wget \
		curl \
		v4l-utils \
	&& rm -rf /var/lib/apt/lists/*
COPY run.sh /
COPY download-hyperion.sh /usr/local/bin/
RUN chmod a+x /run.sh /usr/local/bin/download-hyperion.sh

# Download and install Hyperion using robust download script
RUN echo "Installing Hyperion ${BUILD_VERSION} for ${BUILD_ARCH}..." && \
    /usr/local/bin/download-hyperion.sh "${BUILD_VERSION}" "${BUILD_ARCH}" /usr && \
    \
    # Final verification
    if [ -f /usr/bin/hyperiond ]; then \
        echo "Hyperion installation verified successfully"; \
        /usr/bin/hyperiond --version || echo "Version check failed (may be normal)"; \
    else \
        echo "ERROR: Hyperion daemon not found after installation" >&2; \
        echo "Searching for hyperion binaries..." && \
        find /usr -name "*hyperion*" -type f 2>/dev/null || true; \
        exit 1; \
    fi

VOLUME /config
EXPOSE 8090 8092 19333 19400 19444 19445
CMD [ "/run.sh" ]
