#!/bin/bash

avroUpdate=$1
sqlUpdate=$2

echo "Createtag script start.."
echo "avroUpdate variable: $avroUpdate"
echo "sqlUpdate variable: $sqlUpdate"

#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
IS_TAGGED=`git describe --contains $GIT_COMMIT 2>/dev/null`

#exit if already tag on same commit
if [ -n "$IS_TAGGED" ]; then
  echo "Already a tag on this commit: $IS_TAGGED"
  exit 0
fi

echo "Reading the file gittag.conf.."
VERSION=$(<gittag.conf)

echo "Version input parameter: $VERSION"

#get highest tag number, and add 1.0.0 if doesn't exist
#CURRENT_VERSION=`git describe --abbrev=0 --tags 2>/dev/null`

#if both both variables (avroUpdate + sqlUpdate) equals true - get latest combined version
#elseif variable avroUpdate equals true - get lastest version
#elseif variable sqlUpdate equals true - get lastest version
if [[ $avroUpdate = true ]] && [[ $sqlUpdate = true ]];
then
  CURRENT_VERSION=`git describe --abbrev=0 --tags 2>/dev/null`
  PACKAGETAGVALUE="combined"
  echo "Current Version: $CURRENT_VERSION"
elif [[ $avroUpdate = true ]];
then
  CURRENT_VERSION=`git describe --abbrev=0 --tags 2>/dev/null`
  PACKAGETAGVALUE="sourceschema"
  echo "Current Version: $CURRENT_VERSION"
elif [[ $sqlUpdate = true ]];
then 
  CURRENT_VERSION=`git describe --abbrev=0 --tags 2>/dev/null`
  PACKAGETAGVALUE="sqlddls"
  echo "Current Version: $CURRENT_VERSION"
else
  echo "No change has been done according to variable values.."
  exit 0
fi

regex="^(([0-9]+)\.([0-9]+)\.([0-9]+))$"
if [[ $CURRENT_VERSION =~ $regex ]]; then
  echo "Repo has a previous valid tag"
else
  echo "No valid previous tag"
  CURRENT_VERSION='1.0.0'
fi

echo "Current Version: $CURRENT_VERSION"

#replace . with space so can split into an array
CURRENT_VERSION_PARTS=(${CURRENT_VERSION//./ })

#get number parts
VNUM1=${CURRENT_VERSION_PARTS[0]}
VNUM2=${CURRENT_VERSION_PARTS[1]}
VNUM3=${CURRENT_VERSION_PARTS[2]}

case $VERSION in
  'major')
    VNUM1=$((VNUM1+1))
    VNUM2=0
    VNUM3=0;;
  'minor')
    VNUM2=$((VNUM2+1))
    VNUM3=0;;
  'patch')
    VNUM3=$((VNUM3+1));;
  *)
    echo "No valid version type specified. Make sure gittag.conf contains a vaild value."
    exit 1;;
esac

#create new tag
PACKAGE_NEW_TAG="package-$VNUM1.$VNUM2.$VNUM3-$PACKAGETAGVALUE"
NEW_TAG="$VNUM1.$VNUM2.$VNUM3"
echo "($VERSION) updating $CURRENT_VERSION to $NEW_TAG"
echo "$PACKAGE_NEW_TAG"

#set git identity
git config --global user.email "p986_dck327146@fspa.myntet.se"
git config --global user.name "p986_dck327146"

#tag and push it to repo
git tag -a $NEW_TAG -m "Creating tag with version $NEW_TAG"
git push origin $NEW_TAG
if [ $? = 0 ] ; then
  echo "Tag created and pushed: $NEW_TAG"

  #set output variable
  echo "##vso[task.setvariable variable=ArtifactTag;]$PACKAGE_NEW_TAG"
  exit 0
else
  echo "Git failed."

  #delete local git tag before exit
  git tag -d $NEW_TAG
  exit 1
fi