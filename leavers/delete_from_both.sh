#!/bin/bash
# This script DELETES for given user or domain from ALL (Public and Private) lists.
#
# Syntax ./script_name.sh first.lastname@address.com
# ./script_name.sh firstname.lastname
# ./script_name.sh @domain.com

if [[ $@ ]]; then
  for mailinglist in $(list_lists -b)
    do
	  finduser=$(list_members $mailinglist | grep -io $1)
	  if [[ $? -eq 0 ]] ; then
	    echo "DELETE USER (" $1 ") FROM PUBLIC LIST (" $mailinglist ")"
	    remove_members $mailinglist $1
	  fi
     done
else
  echo "No arguments given"
fi
