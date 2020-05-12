def yes_or_no(message):
	x=input(message)
	while(x!="yes" and x!="no"):
		print("Wrong input Please try again.")
		x=input(message)
	return (x=="yes")



import configparser
config = configparser.ConfigParser()
properties_file='properties.ini'
try:
	config.read(properties_file)
except:
	pass

if not "user" in config:
	email=input("please enter your email: ")
	username=input("please enter your github username: ")
	config["user"]={
	"name":username,
	"email":email
	}
else:
	if not "email" in config["user"]:
		email=input("please enter your email: ")
		config["user"]["email"]=email
	if not "name" in config["user"]:
		username=input("please enter your github username: ")
		config["user"]["name"]=username

import sentry_sdk
from sentry_sdk import configure_scope
with configure_scope() as scope:
    scope.user = {"email": config["user"]["email"]}
sentry_sdk.init("https://51cbbd7414b44db98ebd3b23b68c12ab@o238115.ingest.sentry.io/5238337")
from os import system as execute
from os.path import isdir, basename
from sys import exit

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
with open(properties_file, 'w') as configfile:    # save
	config.write(configfile)