"""Add an email address or regexp to ban_list for all lists.

Save as bin/add_banned.py

Run via

   bin/withlist -a -r add_banned -- <address_to_ban>

where <address_to_ban> is the actual email address or regexp
to be added to ban_list for all lists.
"""

def add_banned(mlist, address):
    if not mlist.Locked():
        mlist.Lock()
    mlist.ban_list.append(address)
    mlist.Save()
    mlist.Unlock()
