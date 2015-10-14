#!/bin/bash

show_anaconda_versions() {
  org=$1
  channel=$2
  echo "executing command: anaconda show $org/$channel"
  anaconda show $org/$channel
}

parse() {
  versions=false
  while read version
  do
    # if this line is blank, it comes after the versions lines
    if [ "$version" == "" ]; then
      versions=false;
    fi;
    # echo "versions is $versions. line is $line"
    if [ $versions == true ] ; then
      echo ${version:2};
    fi;
    # if you find the versions line, you're good to go for the next line
    if [[ "$version" == *"Versions"* ]]; then
      versions=true;
    fi;

  done
}

clean() {
  echo "entering clean() function"
  org=$1
  channel=$2
  clean=$3
  new_version=$4

  echo "org=$org"
  echo "channel=$channel"
  echo "clean=$clean"
  echo "new_version=$new_version"
  while read line
  do
    echo "Removal command --> anaconda remove $org/$channel/$line --force"
    if [ "$line" != "$new_version" ]; then
      if [ $clean == "true" ]; then
        echo "Removing version $version from anaconda.org/$org/$channel";
        anaconda remove $org/$channel/$line --force;
      else
        echo "Would have removed $version from anaconda.org/$org/$channel";
      fi;
    fi;
  done
  echo "leaving clean() function"
}

org=$1
channel=$2
clean=$3
new_version=$4

echo "number of input args = $#"
if [ "$#" == 3 ]; then
  new_version=`cat version`
  # version_string | read -a new_version;
  echo "version_string is $new_version"

elif [ "$#" < 3 ]; then
  echo "
  Illegal number of parameters.

  Usage:

    $0 anaconda-organization anaconda-channel clean new_version.

    anaconda-organization is something like 'lightsource2-dev'
    anaconda-channel is something like 'metadatastore'
    clean is a boolean
    new_version is optional

  Example:

    $0 lightsource2-dev metadatastore true v0.2.0.post55";
  exit
fi;

# echo "Searching https://anaconda.org/$org/$channel"
show_anaconda_versions $org $channel | parse | clean $org $channel $clean $new_version
# show_anaconda_versions $org $channel | parse