#!/usr/bin/python
#
# Given an email address as the parameter, find any
# lists that the email address is an admin for and
# remove them. Mailman is happy for a list to have
# zero owners.

import os
import sys
import subprocess
import tempfile

if len(sys.argv) != 2:
    print "Must specify the email address to remove as admin"

to_remove = sys.argv[1]

# Get the list of lists
process = subprocess.Popen(['list_lists', '-b'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = process.communicate()
list_of_lists = result[0].split('\n')
list_of_lists.remove('')

# Iterate through the lists, looking for any where this person is the admin
for this_list in list_of_lists:
    process = subprocess.Popen(['list_admins', this_list], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = process.communicate()
    admin = result[0].strip().split(": ")
    if len(admin) > 2:
        admin = admin[2].split(", ")
        # Remove the admin we want to lose
        if to_remove in admin:
            admin.remove(to_remove)
            # Now output the revised admin list to a temporary file
            tfile_tuple = tempfile.mkstemp()
            handle = tfile_tuple[0]
            written = os.write(handle, "owner = %s\n" % admin)
            os.close(handle)
            # Tell Mailman to update this list
            process = subprocess.Popen(['config_list', '-i', tfile_tuple[1], this_list], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = process.communicate()
            if result[1] == "":
                print "Removed %s as admin from %s" % (to_remove, this_list)
                if admin == []:
                    print "No admins left for %s" % this_list
            else:
                print "Got error while removing %s as admin from %s: %s" % (to_remove, this_list, result[1])
            # and delete the temp file
            os.remove(tfile_tuple[1])
