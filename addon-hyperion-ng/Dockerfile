FROM ghcr.io/home-assistant/base-debian:bookworm-2026.06.0

ARG BUILD_VERSION
ARG BUILD_ARCH

ENV LANG=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
		libavahi-core7 \
		libavahi-compat-libdnssd1 \
		libusb-1.0-0 \
		libudev1 \
		libexpat1 \
		libfontconfig1 \
		libglib2.0-0 \
		zlib1g \
		libcec6 \
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
        /usr/bin/hyperiond --version; \
    else \
        echo "ERROR: Hyperion daemon not found after installation" >&2; \
        echo "Searching for hyperion binaries..." && \
        find /usr -name "*hyperion*" -type f 2>/dev/null || true; \
        exit 1; \
    fi && \
    ldd_output="$(ldd /usr/share/hyperion/bin/hyperiond)" && \
    printf '%s\n' "$ldd_output" && \
    ! printf '%s\n' "$ldd_output" | grep -F "not found"

VOLUME /config
EXPOSE 8090 8092 19333 19400 19444 19445
CMD [ "/run.sh" ]
