#!/bin/bash

BUILD_DIR=$(pwd)/build
MESSAGE="automatic build"

mkdir -p $BUILD_DIR

cat <<DEBUILD > debuild.sh
mkdir -p build
rm -f debian/changelog
dch --package pywebdriver --newversion $(date +%Y%m%d) --create -m "$MESSAGE"
debuild
cp ../*.deb /build
DEBUILD
chmod +x debuild.sh

cat <<DOCKERFILE > Dockerfile
FROM ubuntu:18.04
COPY . /pywebdriver
WORKDIR /pywebdriver
RUN apt-get update && apt-get install -y debhelper dh-virtualenv dh-systemd devscripts python-wheel libcups2-dev python-dev
DOCKERFILE

docker build -t pywebdriver_build .
docker run -v $BUILD_DIR:/build -it pywebdriver_build bash -c "./debuild.sh"
