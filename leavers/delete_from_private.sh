#!/bin/bash
# This script DELETES for given user or domain from PRIVATE lists.
#
# Syntax ./script_name.sh first.lastname@address.com
# ./script_name.sh firstname.lastname
# ./script_name.sh @domain.com

if [[ $@ ]]; then
  for mailinglist in $(comm -23 <(list_lists -b) <(list_lists -b -a))
    do
      finduser=$(list_members $mailinglist | grep $1 |  awk '{print}')
      if [[ -n $finduser ]];  then
         array=($finduser);
         echo "Found ${#array[*]} USERS for PRIVATE LIST $mailinglist"@"$NICKNAME";
         for ((i=0; i<${#array[*]}; i++));
           do
             read -p "Are you sure you want to delete ${array[$i]} from $mailinglist@$NICKNAME?" -n 1 -r
             echo
             if [[ $REPLY =~ ^[Yy]$ ]]; then
               echo "DELETED ${array[$i]} FROM PRIVATE LIST $mailinglist"@"$NICKNAME";
               remove_members $mailinglist ${array[$i]}
             else
               echo "Did NOT delete ${array[$i]} from $mailinglist@$NICKNAME"
             fi
           done
      fi
    done
else
  echo "No arguments given."
  echo -e "Syntax: \n ./script_name.sh first.lastname@address.com  \n ./script_name.sh firstname.lastname \n ./script_name.sh @domain.com"
fi