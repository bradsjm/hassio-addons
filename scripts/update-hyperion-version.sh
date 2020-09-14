#!/bin/sh
set -ex

BASE=${GITHUB_WORKSPACE}/addon-hyperion-ng

FILE="${BASE}/config.json"
CURRENT="$(jq -r ".version" $FILE)"

REPO="https://github.com/hyperion-project/hyperion.ng.git"
RELEASE="$(git ls-remote --tags ${REPO} | cut -d/ -f3- | tail -n1)"

if [ "${CURRENT}" != "${RELEASE}" ]; then
    jq ".version=\"${RELEASE}\"" $FILE > $FILE.tmp
    mv $FILE.tmp $FILE
    exit 0
fi

exit 1