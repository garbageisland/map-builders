#!/bin/bash

shopt -s nullglob

logFolders () {
  # Die if no directory is provided
  [[ $# -eq 0 ]] && { echo "Usage: $0 dir-name"; exit 1; }

  for i in $1/*;
  do
    if [ -d $i ]
    then
      echo "into $i"

      files=( $i/*.png$ )
      (( ${#files[@]} )) && convert -delay 1/24 -loop 0  -dispose background -coalesce -alpha on $i/*.png $i/anim.gif && chown justin:www-data $i/anim.gif && chmod 0664 $i/anim.gif && echo "---- gif created"

      logFolders $i
    else
      if [[ "$i" == *"png"* ]]
      then
        #echo "no delete"
        rm $i 
      fi
    fi
  done
}

logFolders $1

shopt -u nullglob