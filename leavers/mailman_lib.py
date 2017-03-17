"""Shared code to handle removing admins from lists."""

import os
import subprocess
import tempfile

def remove_admin(to_remove):
    output = ""
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
                    output += "Removed %s as admin from %s\r\n" % (to_remove, this_list)
                    if admin == []:
                        output += "NOTE! No admins left for %s\r\n" % this_list
                else:
                    output += "Got error while removing %s as admin from %s: %s\r\n" % (to_remove, this_list, result[1])
                # and delete the temp file
                os.remove(tfile_tuple[1])

    return output

def remove_member(to_remove):
    output = ""
    # Get the list of lists
    process = subprocess.Popen(['list_lists', '-b'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = process.communicate()
    list_of_lists = result[0].split('\n')
    list_of_lists.remove('')

    # Iterate through the lists, looking for any where this person is the admin
    for this_list in list_of_lists:
        process = subprocess.Popen(['list_members', this_list], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.communicate()
        members = result[0].strip().split('\n')
            # Remove the member we want to lose
            if to_remove in members:
                process = subprocess.Popen(['remove_members', this_list, to_remove], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = process.communicate()
                if result[0] != "":
                    output += "Error while removing from %s: %s\r\n" % (this_list, result[0])
                else:
                    output += "Removed %s as member from %s\r\n" % (to_remove, this_list)

    return output
