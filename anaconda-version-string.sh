version_string () {
  debug=$1
  read -a path
  if [ $debug ]; then
    echo "
  full file path:
  $path
  ";
  fi;
  IFS="/"; declare -a version_split=($path)

  if [ $debug ]; then
  echo "
  file name:
  ${version_split[-1]}
  ";
  fi;

  IFS="-"; declare -a version_string_split=(${version_split[-1]})

  if [ $debug ]; then
  echo "version string:
  ";
  fi;
  echo ${version_string_split[1]}
}

version_string $1