#!/bin/bash

set -ev

if [[ $1 == "dev" ]]
then
    DEPLOY_SCRIPT=$DEPLOY_SCRIPT_DEV
elif [[ $1 == "prod" ]]
    DEPLOY_SCRIPT=$DEPLOY_SCRIPT_PROD
else
    DEPLOY_SCRIPT="echo No Script Specified!"
fi

openssl aes-256-cbc -K $encrypted_7df0bf92a043_key -iv $encrypted_7df0bf92a043_iv -in $TRAVIS_BUILD_DIR/.travis/ssh_key.enc -out $TRAVIS_BUILD_DIR/.travis/ssh_key -d
chmod 600 $TRAVIS_BUILD_DIR/.travis/ssh_key
ssh -i $TRAVIS_BUILD_DIR/.travis/ssh_key -o StrictHostKeyChecking=no travis@$DEPLOY_HOST_IP $DEPLOY_SCRIPT
