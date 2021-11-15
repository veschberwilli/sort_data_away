####################################################################
# script to scan folder structure and adapt naming
# i.e. removing whitespaces and Umlaute in names

# Author: Michael Mink
# Date: 11/2019

# Dependencies:
# - exiftool

####################################################################

# import packages
import os

#path_data = '/home/egon/veschberwilli/sort_pics/pics_unsorted'
path_data = '/media/pi/egon/data_all_unsorted'

# ++++++++++++++++++++++++++++++
# search directories recursively
# substitute whitespace with _
# ++++++++++++++++++++++++++++++
for (path,dirs,files) in os.walk(path_data):

    if path.find(' ') != -1:
        path_updated = path.replace(' ', '_')
        os.system('mv "%s" "%s"' % (path, path_updated))

        print('space removed: "%s" --> "%s"' % (path, path_updated))

# ++++++++++++++++++++++++++++++
# search directories recursively
# substitute Umlaute
# ++++++++++++++++++++++++++++++
forbidden_chars = {
    'ä': 'ae',
    'Ä': 'Ae',
    'ö': 'oe',
    'Ö': 'Oe',
    'ü': 'ue',
    'Ü': 'Ue',
    '%': '_',
    '&': '_',
    '(': '_',
    ')': '_',
    '=': '_',
}

# ++++++++++++++++++++++++++++++
# search directories recursively
# substitute Umlaute
# ++++++++++++++++++++++++++++++
for (path,dirs,files) in os.walk(path_data):
    for check in forbidden_chars:
        if path.find(check) != -1:
            path_updated = path.replace(check, forbidden_chars[check])
            os.system('mv "%s" "%s"' % (path, path_updated))

            print('Umlaut removed: %s --> %s' % (path, path_updated))


# ++++++++++++++++++++++++++++++
# search directories recursively
# correct file names
# ++++++++++++++++++++++++++++++
for (path,dirs,files) in os.walk(path_data):
    # get files in directory
    for file in files:

        file_path = os.path.join(path, file)

        # replace spaces by _
        if file.find(' ') != -1:
            file_updated = file.replace(' ', '_')
            file_path_updated = os.path.join(path, file_updated)
            os.system('mv "%s" "%s"' % (file_path, file_path_updated))

        # remove (
        if file.find('(') != -1:
            file_updated = file.replace('(', '')
            file_path_updated = os.path.join(path, file_updated)
            os.system('mv "%s" "%s"' % (file_path, file_path_updated))

        # remove )
        if file.find(')') != -1:
            file_updated = file.replace(')', '')
            file_path_updated = os.path.join(path, file_updated)
            os.system('mv "%s" "%s"' % (file_path, file_path_updated))
