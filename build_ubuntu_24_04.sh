#!/bin/bash
set -e

# ONLY use this to test builds. Actual build should be done by github actions

BUILD_DIR=$(pwd)/build
MESSAGE="automatic build"
PACKAGE="pywebdriver"
BASE_IMAGE=ubuntu:24.04
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
RUN apt-get update && apt-get install -y software-properties-common
RUN DEBIAN_FRONTEND=noninteractive TZ=Europe/Paris apt-get -y install tzdata
RUN apt-get update && apt-get install -y debhelper dh-python dh-virtualenv devscripts python3-wheel libcups2-dev python3-setuptools libmtp-dev libffi-dev python3-venv python3-pip python3-simplejson python3-flask-babel python3-flask-cors python3-usb python3-serial python3-netifaces python3-cups python3-pillow
#COPY . /$PACKAGE
WORKDIR /$PACKAGE
DOCKERFILE

read -p "Build Docker image? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker pull $BASE_IMAGE
    docker build -t ${PACKAGE}_build .
fi

read -p "Buid $PACKAGE package? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker run -v $(pwd):/$PACKAGE -v $BUILD_DIR:/build -it ${PACKAGE}_build bash -c "./debuild.sh"
fi
