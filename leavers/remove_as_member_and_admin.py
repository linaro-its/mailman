#!/usr/bin/python
#
# Given an email address as the parameter, find any lists where the email
# address is a member or an admin and remove them.

import sys
import mailman_lib

if len(sys.argv) != 2:
    print "Must specify the email address to remove"

to_remove = sys.argv[1]

result = mailman_lib.remove_admin(to_remove)
result += mailman_lib.remove_member(to_remove)

print result
