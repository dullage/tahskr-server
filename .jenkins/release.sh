#!/bin/bash

set -e

tag=$(cat $WORKSPACE/app/VERSION)

printf "Creating Release...\n"
curl -fsS \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"tag_name\": \"$tag\", \"target_commitish\": \"master\", \"name\": \"$tag\"}" \
    https://api.github.com/repos/$GIT_REPO_SLUG/releases
