#!/bin/bash
set -e

BUILD_DIR=$(pwd)/build
MESSAGE="automatic build"
PACKAGE="pywebdriver"
DISTRIBUTION=pywebdriver-nightly
REPO=apt.akretion.com
BASE_IMAGE=ubuntu:18.04
KEY=

mkdir -p $BUILD_DIR

cat <<DEBUILD > debuild.sh
mkdir -p build
rm -f debian/changelog
dch --package $PACKAGE --newversion $(date +%Y%m%d) --create -m "$MESSAGE"
debuild
cp ../${PACKAGE}_* /build
DEBUILD
chmod +x debuild.sh

cat <<DOCKERFILE > Dockerfile
FROM $BASE_IMAGE
RUN apt-get update && apt-get install -y debhelper dh-virtualenv dh-systemd devscripts python3-wheel libcups2-dev python3-setuptools libmtp-dev python3-pip libffi-dev
COPY . /$PACKAGE
WORKDIR /$PACKAGE
DOCKERFILE

read -p "Buid $PACKAGE package? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker pull $BASE_IMAGE
    docker build -t ${PACKAGE}_build .
    docker run -v $BUILD_DIR:/build -it ${PACKAGE}_build bash -c "./debuild.sh"
fi

read -p "Publicsh $PACKAGE package on $REPO $DISTRIBUTION (y/n) "
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -rf ~/.aptly
    aptly repo create $REPO
    aptly repo add $REPO build
    SNAPSHOT_NAME=$DISTRIBUTION-$(date +%Y%m%d)
    aptly snapshot create $SNAPSHOT_NAME from repo $REPO
    # publish using aptly https://www.aptly.info/ on amazon S3 endpoint
    # whith the current repository configuration in ~/aptly.conf:
    # "S3PublishEndpoints": {
    #   "apt.akretion.com": {
    #     "bucket": "apt.akretion.com",
    #     "endpoint": "https://s3.amazonaws.com",
    #     "awsAccessKeyID": "XXXXXXXX",
    #     "awsSecretAccessKey": "XXXXXXXX"
    #    }
    # for sign the repository you need a gpg key: https://help.ubuntu.com/community/GnuPrivacyGuardHowto
    # you also need to put the following paramaters in your gpg configuration (~/.gnupg/gpg.conf)
    # personal-digest-preferences SHA256
    # cert-digest-algo SHA256
    # default-preference-list SHA512 SHA384 SHA256 SHA224 AES256 AES192 AES CAST5 ZLIB BZIP2 ZIP Uncompressed
    aptly publish snapshot -distribution="$DISTRIBUTION" $SNAPSHOT_NAME s3:$REPO:
    echo "here it is the commands to install $PACKAGE pywebdriver from $REPO:"
    echo
    echo "sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com XXXXXXXX"
    echo "sudo apt-add-repository 'deb [arch=amd64] http://$REPO/ $DISTRIBUTION main'"
    echo "sudo apt-get update"
    echo "sudo apt-get install $PACAKGE"
fi
