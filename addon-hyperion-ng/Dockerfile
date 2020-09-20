ARG BUILD_TAG
ARG BUILD_FROM
ARG BUILD_ARCH

# Use Hyperion CI Image defined in build.json to build from source
FROM ${BUILD_FROM}:${VERSION_TAG} as build
ARG BUILD_VERSION
ARG GIT_REPO_URL
RUN git clone --recursive --depth 1 -q ${GIT_REPO_URL} /hyperion
RUN /bin/bash -c "cd /hyperion && mkdir build && cd build && \
	cmake -DCMAKE_BUILD_TYPE=Release .. || exit 2 && \
	make -j $(nproc) || exit 3 && \
    strip /hyperion/build/bin/h* && \
	exit 0; \
	exit 1" || { echo "---> Hyperion compilation failed! Abort"; exit 4; }


# Use Home Assistant Debian base image for addon runtime
FROM homeassistant/${BUILD_ARCH}-base-debian:${VERSION_TAG}
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
		libturbojpeg0 \
		libssl1.1 \
		zlib1g \
		libcec4 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /hyperion/build/bin/h* /hyperion/
COPY run.sh /
RUN chmod a+x /run.sh
WORKDIR /hyperion
VOLUME /config
EXPOSE 8090 8092 19333 19400 19444 19445
CMD [ "/run.sh" ]