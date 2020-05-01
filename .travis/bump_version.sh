#!/bin/bash

set -ev

git config --global user.email "travis@travis-ci.com"
git config --global user.name "Travis CI"

git checkout master

python ./.travis/bump_version.py ./app/version.json

VERSION=$(cat version.json | jq -r ".version")

git add .
git commit -m "$VERSION_BUMP_MESSAGE_PREFIX $VERSION"

git tag -a $VERSION -m "$VERSION"

git remote add origin-authenticated https://${GITHUB_TOKEN}@github.com/$GIT_REPO_SLUG.git
git push --set-upstream origin-authenticated --follow-tags master
