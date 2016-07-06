import os

find = raw_input("Enter the phrase to be replaced   ")
replace = raw_input("Enter the phrase to be substituted   ")
directory = raw_input("Enter the directory")
if not directory.endswith("/"):
    directory = directory + "/"

for fil in os.listdir(directory):
    fileName = directory + fil
    if find in fileName:
        replacementFileName = fileName.replace(find, replace)
        print "renaming"
        os.system("mv \"" + fileName + "\" \"" + replacementFileName + "\"")