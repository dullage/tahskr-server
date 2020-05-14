#!/bin/bash

set -e

if [[ $BRANCH_NAME == "master" ]]
then
    deploy_script=/home/dullage/tahskr/server/prod/deploy.sh
elif [[ $BRANCH_NAME == "develop" ]]
then
    deploy_script=/home/dullage/tahskr/server/dev/deploy.sh
else
    echo Invalid Branch: $BRANCH_NAME
    exit 1
fi

ssh -i $SSH_KEY -o StrictHostKeyChecking=no jenkins@$DEPLOY_IP $deploy_script
