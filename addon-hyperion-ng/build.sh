#!/bin/sh
set -ex

BASE=$(cd "$(dirname "$0")"; pwd)
FILE="${BASE}/config.json"
CURRENT="$(jq -r ".version" $FILE)"

REPO="https://github.com/hyperion-project/hyperion.ng.git"
RELEASE="$(git ls-remote --tags ${REPO} | cut -d/ -f3- | tail -n1)"

if [ "${CURRENT}" != "${RELEASE}" ]; then
    jq ".version=\"${RELEASE}\"" $FILE > $FILE.tmp
    mv $FILE.tmp $FILE
    git add $FILE
    git commit -m "Updated version to ${RELEASE}"
    git push origin
fi

docker run --rm --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v ~/.docker:/root/.docker \
    -v ${BASE}:/data \
    homeassistant/amd64-builder \
    --target /data \
    --no-cache \
    --docker-user "${DOCKER_USER}" \
    --docker-password "${DOCKER_PASSWORD}" \
    --docker-hub-check \
    --${ARCH}
