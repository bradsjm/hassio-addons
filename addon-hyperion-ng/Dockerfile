ARG BUILD_ARCH

FROM homeassistant/${BUILD_ARCH}-base-debian
ARG DOWNLOAD_URL
ARG BUILD_VERSION
ARG BUILD_FROM

ENV LANG C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
		libpython3.7 \
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
		libcec4 \
		wget \
    && rm -rf /var/lib/apt/lists/*
COPY run.sh /
RUN chmod a+x /run.sh

ENV PKG ${DOWNLOAD_URL}/${BUILD_VERSION}/Hyperion-${BUILD_VERSION}-${BUILD_FROM}
RUN wget -q -O /tmp/hyperion.deb ${PKG} && \
	dpkg --force architecture -i /tmp/hyperion.deb && \
	rm /tmp/hyperion.deb

VOLUME /config
EXPOSE 8090 8092 19333 19400 19444 19445
CMD [ "/run.sh" ]