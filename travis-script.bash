#!/bin/bash
set -euo pipefail
# Used by travis to trigger deployments or builds
# Keeping this here rather than make travis.yml too complex

ACTION="${1}"
PUSH=''
if [[ ${ACTION} == 'build' ]]; then
    if [[ ${TRAVIS_PULL_REQUEST} == 'false' ]]; then
        PUSH='--push'
        # Assume we're in master and have secrets!
        docker login -u $DOCKER_USERNAME -p "$DOCKER_PASSWORD"
    fi

    ./deploy.py build --commit-range ${TRAVIS_COMMIT_RANGE} ${PUSH}
elif [[ ${ACTION} == 'deploy' ]]; then
    REPO="https://github.com/${TRAVIS_REPO_SLUG}"
    CHECKOUT_DIR="/tmp/${TRAVIS_BUILD_NUMBER}"
    COMMIT="${TRAVIS_COMMIT}"
    MASTER_HOST="datahub-fa17-${TRAVIS_BRANCH}.westus2.cloudapp.azure.com"


    openssl aes-256-cbc -K $encrypted_eee6172de5ea_key -iv $encrypted_eee6172de5ea_iv -in sshkey.enc -out sshkey -d
    chmod 0400 sshkey

    ssh -i sshkey \
        -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
        datahub@${MASTER_HOST} \
        "git clone ${REPO} ${CHECKOUT_DIR} && cd ${CHECKOUT_DIR} && git crypt unlock /etc/deploy-secret-keyfile && git checkout ${COMMIT} && ./deploy.py deploy datahub; rm -rf ${CHECKOUT_DIR}"
    rm -rf sshkey
fi
