#!/usr/bin/env bash
DIST_NAME=pywebdriver
DIST_TYPE=tar.gz
DIST_DIR=dist
BUILD_DIR=build

read -p "Full Dev name: " fullname
read -p "Email: " email
default_version=$(cat VERSION)-1
read -p "Version: (default $default_version): " version
version=${version:-$default_version}
export DEBFULLNAME=$fullname
export DEBEMAIL=$email
debchange -v $version

rm -rf $DIST_DIR $BUILD_DIR
python setup.py sdist
DIST_FILENAME=$(ls $DIST_DIR/*.$DIST_TYPE -1 | tail -n 1 | cut -d'/' -f2)
ORIG_FILENAME=$(echo $DIST_FILENAME | sed "s/$DIST_TYPE/orig.$DIST_TYPE/" | sed "s/\-/_/")

cp config/config.ini debian/config.ini
cp $DIST_DIR/$DIST_FILENAME ../$ORIG_FILENAME
rm -rf $DIST_DIR $BUILD_DIR

debuild -i -us -uc -b

#cleanup
rm debian/config.ini
debclean
