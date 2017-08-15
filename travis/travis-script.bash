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
    echo "Starting deploy..."
    REPO="https://github.com/${TRAVIS_REPO_SLUG}"
    CHECKOUT_DIR="/tmp/${TRAVIS_BUILD_NUMBER}"
    COMMIT="${TRAVIS_COMMIT}"
    MASTER_HOST="datahub-fa17-${TRAVIS_BRANCH}.westus2.cloudapp.azure.com"
    MASTER_HOST="datahub-fa17-${TRAVIS_BRANCH}.westus2.cloudapp.azure.com"
    SSHKEY="sshkey-${TRAVIS_BRANCH}"

    echo "Fetching ssh key..."
    # Travis only allows encrypting one file per repo. LAME
    openssl aes-256-cbc -K $encrypted_0f80927fa736_key -iv $encrypted_0f80927fa736_iv -in travis/ssh-keys.tar.gz.enc -out travis/ssh-keys.tar.gz -d
    tar xvf travis/ssh-keys.tar.gz

    chmod 0400 "${SSHKEY}"

    echo "SSHing..."
    ssh -i "${SSHKEY}"\
        -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
        datahub@${MASTER_HOST} \
        "git clone ${REPO} ${CHECKOUT_DIR} && cd ${CHECKOUT_DIR} && git checkout ${COMMIT} && git crypt unlock /etc/deploy-secret-keyfile && ./deploy.py deploy ${TRAVIS_BRANCH}; rm -rf ${CHECKOUT_DIR}"
    rm -rf "sshkey-*"

    echo "Done!"
fi
