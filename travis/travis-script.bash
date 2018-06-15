#!/bin/bash
# vim: set et sw=4 ts=4:
set -euo pipefail

# Used by travis to trigger deployments or builds
# Keeping this here rather than make travis.yml too complex

# .travis.yml:
# - AZ_LOCATION
# - DOCKER_PASSWORD (secure)
# - DOCKER_USERNAME (secure)
# - GIT_CRYPT_KEY_64 (secure)
# - SUBSCRIPTION_PREFIX
# travis project settings:
# - encrypted_0f80927fa736_key (created by 'travis encrypt-file')
# - encrypted_0f80927fa736_iv  (created by 'travis encrypt-file')

function prepare_azure {
    SP="${TRAVIS_BUILD_DIR}/hub/secrets/sp-${TRAVIS_BRANCH}.json"
    if [ ! -f ${SP} ]; then
        echo "Could not find service principal file: ${SP}"
        echo find ${TRAVIS_BUILD_DIR}
        find ${TRAVIS_BUILD_DIR}
        exit 1
    else
        echo "Found service principal file: ${SP}"
    fi

    echo service principal user: $(jq -r .name ${SP})
    az login --service-principal \
              -u $(jq -r .name     ${SP}) \
              -p $(jq -r .password ${SP}) \
        --tenant $(jq -r .tenant   ${SP}) > /dev/null
    az account set -s ${SUBSCRIPTION_PREFIX}-${TRAVIS_BRANCH} > /dev/null
    az account show --query=name
}

ACTION="${1}"
PUSH=''
if [[ ${ACTION} == 'build' ]]; then
    if [[ ${TRAVIS_PULL_REQUEST} == 'false' ]]; then
        # In this context we have travis secrets!
        PUSH='--push'
        echo "Logging in to docker hub"
        docker login -u $DOCKER_USERNAME -p "$DOCKER_PASSWORD"

        ## This is all just so that we can run kubectl to deploy a daemonset.
        ## Later we can run helm during deploy rather than ssh.
        echo ${GIT_CRYPT_KEY_64} | base64 -d > ./git-crypt.key
        chmod 0400 git-crypt.key
        git-crypt unlock git-crypt.key

        export KUBECONFIG="${TRAVIS_BUILD_DIR}/hub/secrets/kc-${TRAVIS_BRANCH}-${AZ_LOCATION}.json"
        echo KUBECONFIG="${KUBECONFIG}" md5sum=$(md5sum ${KUBECONFIG})
        echo /usr/local/bin/kubectl get nodes
        /usr/local/bin/kubectl get nodes
        prepare_azure
    fi

    # Attempt to improve relability of pip installs:
    # https://github.com/travis-ci/travis-ci/issues/2389
    sudo sysctl net.ipv4.tcp_ecn=0

    ./deploy.py build --commit-range ${TRAVIS_COMMIT_RANGE} ${PUSH}
elif [[ ${ACTION} == 'deploy' ]]; then
    echo "Starting deploy..."
    REPO="https://github.com/${TRAVIS_REPO_SLUG}"
    CHECKOUT_DIR="/tmp/${TRAVIS_BUILD_NUMBER}"
    COMMIT="${TRAVIS_COMMIT}"
    MASTER_HOST="datahub-fa17-${TRAVIS_BRANCH}.${AZ_LOCATION}.cloudapp.azure.com"
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
        "rm -rf ${CHECKOUT_DIR} && git clone ${REPO} ${CHECKOUT_DIR} && cd ${CHECKOUT_DIR} && git checkout ${COMMIT} && git crypt unlock /etc/deploy-secret-keyfile && ./deploy.py deploy ${TRAVIS_BRANCH} && rm -rf ${CHECKOUT_DIR}"
    rm -rf "sshkey-*"

    echo "Done!"
fi
