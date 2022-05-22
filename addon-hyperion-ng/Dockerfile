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
		v4l-utils \
	&& rm -rf /var/lib/apt/lists/*
COPY run.sh /
RUN chmod a+x /run.sh

RUN wget -q "${DOWNLOAD_URL}/${BUILD_VERSION}/Hyperion-${BUILD_VERSION}-Linux-$(uname -m).tar.gz" -O - | tar -xvz -C /usr

VOLUME /config
EXPOSE 8090 8092 19333 19400 19444 19445
CMD [ "/run.sh" ]
