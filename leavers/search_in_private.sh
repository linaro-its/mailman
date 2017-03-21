#!/bin/bash
# This script searches for given user or domain from *PRIVATE* lists.
#
# Syntax ./script_name.sh first.lastname@address.com
# ./script_name.sh firstname.lastname
# ./script_name.sh @domain.com

if [[ $@ ]]; then
  for mailinglist in $(comm -23 <(list_lists -b) <(list_lists -b -a))
    do
      finduser=$(list_members $mailinglist | grep $1 |  awk '{print}')
      if [[ -n $finduser ]];  then
        echo FOUND $finduser IN $mailinglist"@"$NICKNAME
      fi
     done
 else
    echo "No arguments given"
    echo -e "Syntax: \n ./script_name.sh first.lastname@address.com  \n ./script_name.sh firstname.lastname \n ./script_name.sh @domain.com"
fi
