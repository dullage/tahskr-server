#!/bin/bash

set -ev

VERSION=$(cat version.json | jq -r ".version")
ARCH=$1
PUSH=$2

docker build -t $DOCKER_REPO_SLUG:$VERSION-$ARCH $TRAVIS_BUILD_DIR

if [[ $PUSH == push ]]
then
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    docker push $DOCKER_REPO_SLUG:$VERSION-$ARCH
fi
