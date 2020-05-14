#!/bin/bash

set -e

git config user.email "jenkins@jenkins.io"
git config user.name "Jenkins"

version=$(cat $WORKSPACE/app/version)

git fetch --tags
existing_tag_count=$(git tag | grep $version | wc -l)

if [[ $existing_tag_count == 0 ]]
then
    git tag -a "$version" -m "$version"

    git remote add origin-authenticated https://${GITHUB_TOKEN}@github.com/$GIT_REPO_SLUG.git
    git push origin-authenticated $version
else
    echo "Tag Already Exists: $version"
    exit 1
fi
