from os import system as execute
from os.path import isdir, basename
from sys import exit

def yes_or_no(message):
	x=input(message)
	while(x!="yes" and x!="no"):
		print("Wrong input Please try again.")
		x=input(message)
	return (x=="yes")

if not (isdir('./.git')):
	x=yes_or_no("Do you want to create a new git repository here?(yes/no) ")
	if (x):
		link=input("Please enter the repository you want to clone(https link prefered): ")
		execute("git clone {}".format(link))
		folder_created=link.split("/")[-1].split(".")[0]
		#print(folder_created)
		execute("cp {} ./{}/{}".format(basename(__file__),folder_created,basename(__file__)))
	else:
		print("I cannot run the settings here. You need to run this script in a repository.")
		exit(1)
else:
	upload=yes_or_no("Do you want to upload to git?(yes/no) ")
	if upload:
		execute("git add .")
		message=input("Please enter a message for the upload: ")
		try:
			execute("git commit -m '{}'".format(message))
		except:
			pass
		execute("git push")
