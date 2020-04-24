#!/bin/bash

set -ev

VERSION=$(cat version.json | jq -r ".version")

export DOCKER_CLI_EXPERIMENTAL="enabled"
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Create Manifests
docker manifest create $DOCKER_REPO_SLUG:$VERSION $DOCKER_REPO_SLUG:$VERSION-amd64 $DOCKER_REPO_SLUG:$VERSION-arm64
docker manifest create $DOCKER_REPO_SLUG:latest $DOCKER_REPO_SLUG:$VERSION-amd64 $DOCKER_REPO_SLUG:$VERSION-arm64

# Push Manifests
docker manifest push $DOCKER_REPO_SLUG:$VERSION
docker manifest push $DOCKER_REPO_SLUG:latest
