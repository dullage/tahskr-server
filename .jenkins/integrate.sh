#!/bin/bash

set -e

if [[ $BRANCH == "master" ]]
then
    deploy_script=/home/dullage/tahskr/server/prod/deploy.sh
elif [[ $BRANCH == "develop" ]]
then
    deploy_script=/home/dullage/tahskr/server/dev/deploy.sh
fi

ssh -i $SSH_KEY -o StrictHostKeyChecking=no jenkins@$DEPLOY_IP $deploy_script
