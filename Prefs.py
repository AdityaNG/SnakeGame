import os

'''
prefs.py
This files handles:
    1. Setting prefs
    2. Getting prefs
    3. Dropping prefs
'''

destfolder = "scores/"
if not os.path.exists(destfolder):
    os.makedirs(destfolder)


def get_pref(p):
    current_pref = destfolder + p + ".txt"
    file_exists = os.path.isfile(current_pref)

    if not file_exists:
        f=open(current_pref, "w")
        f.write("")
        f.close()
        return ""

    f=open(current_pref, "r")

    if f.mode == 'r':
        return f.read()
    else:
        print("Permission Error : ", current_pref)
        exit(1)

def get_all_prefs():
    for p in os.listdir(destfolder):
        print(p)
        current_pref = destfolder + p + ".txt"
        file_exists = os.path.isfile(current_pref)

        if not file_exists:
            f=open(current_pref, "w")
            f.write("")
            f.close()
            return ""

        f=open(current_pref, "r")

        if f.mode == 'r':
            return f.read()
        else:
            print("Permission Error : ", current_pref)
            exit(1)

def set_pref(p, val):
    current_pref = destfolder + p + ".txt"
    f=open(current_pref, "w")
    f.write(val)
    f.close()

def drop_pref(p):
    current_pref = destfolder + p + ".txt"
    f=open(current_pref, "w")
    f.write("")
    f.close()
