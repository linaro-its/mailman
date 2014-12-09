#!/bin/bash
# This script DELETES for given user or domain from PUBLIC lists ONLY.
#
# Syntax ./script_name.sh first.lastname@address.com
# ./script_name.sh firstname.lastname
# ./script_name.sh @domain.com

if [[ $@ ]]; then
  for mailinglist in $(list_lists -b -a)
    do
      finduser=$(list_members $mailinglist | grep $1 |  awk '{print}')
      if [[ -n $finduser ]];  then
         array=($finduser);
         echo "FOUND ${#array[*]} users FOR list $mailinglist"@"$NICKNAME";
         for ((i=0; i<${#array[*]}; i++));
           do
             read -p "Are you sure you want to DELETE ${array[$i]} FROM PUBLIC LIST $mailinglist@$NICKNAME?" -n 1 -r
             echo
             if [[ $REPLY =~ ^[Yy]$ ]]; then
               echo "DELETED ${array[$i]} FROM PUBLIC list $mailinglist"@"$NICKNAME";
               remove_members $mailinglist ${array[$i]}
             else
               echo "Did NOT delete ${array[$i]} FROM $mailinglist@$NICKNAME"
             fi
           done
      fi
    done
else
  echo "No arguments given."
  echo -e "Syntax: \n ./script_name.sh first.lastname@address.com  \n ./script_name.sh firstname.lastname \n ./script_name.sh @domain.com"
fi