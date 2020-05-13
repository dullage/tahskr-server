#!/bin/bash

set -e

git config user.email "jenkins@jenkins.io"
git config user.name "Jenkins"

git fetch --tags
existing_tag_count=$(git tag | grep $VERSION | wc -l)

if [[ $existing_tag_count == 0 ]]
then
    git tag -a "$VERSION" -m "$VERSION"

    git remote add origin-authenticated https://${GITHUB_TOKEN}@github.com/$GIT_REPO_SLUG.git
    git push origin-authenticated $VERSION
else
    echo "Tag Already Exists: $VERSION"
    exit 1
fi
