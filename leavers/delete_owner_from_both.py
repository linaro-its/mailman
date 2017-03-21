#!/usr/bin/python
#
# Given an email address as the parameter, find any
# lists that the email address is an admin for and
# remove them. Mailman is happy for a list to have
# zero owners.

import sys
import mailman_lib

if len(sys.argv) != 2:
    print "Must specify the email address to remove as admin"
    return

to_remove = sys.argv[1]

print mailman_lib.remove_admin(to_remove)
