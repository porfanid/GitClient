from os import system as execute
from os.path import isdir, basename, abspath, sep
from sys import exit
import sentry_sdk
from sentry_sdk import configure_scope
sentry_sdk.init("https://51cbbd7414b44db98ebd3b23b68c12ab@o238115.ingest.sentry.io/5238337")
import configparser


def yes_or_no(message):
	x=input(message)
	while(x!="yes" and x!="no"):
		print("Wrong input Please try again.")
		x=input(message)
	return (x=="yes")


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


with configure_scope() as scope:
    scope.user = {"email": config["user"]["email"]}

selected_repository_dir=None
if not (isdir('.git')):
	x=yes_or_no("Do you want to create a new git repository here?(yes/no) ")
	if (x):
		link=input("Please enter the repository you want to clone(https link prefered): ")
		link="https://"+config["user"]["name"]+"@"+link.split("https://")[-1]
		execute("git clone {}".format(link))
		folder_created=link.split(sep)[-1].split(".")[0]
		if "repositories" not in config:
			config["repositories"]={folder_created:abspath(folder_created)}
		else:
			config["repositories"][folder_created]=abspath(folder_created)
	else:
		if not "repositories" in config:
			open=yes_or_no("Do you want to open an existing repository?(yes/no) ")
			if open:
				while True:
					dir=input("Please enter the path to the directory where the repository is located: ")
					if not isdir("{}{}.git".format(dir,sep)):
						go_on=yes_or_no("Wrong Option.\n Do you want to try again?(yes/no) ")
						if not go_on:
							exit(0)

			print("Cannot continue. Exiting")
			exit(0)
		print("")
		for repository in config["repositories"]:
			print("{}:{}".format(repository,config["repositories"][repository]))
		print("")
		while True:
			try:
				x=input("Please select a repository: ")
				selected_repository_dir=config["repositories"][x]
				break
			except:
				print("Wrong repository. Please try again.")
else:
	selected_repository_dir="./"
upload=yes_or_no("Do you want to upload to git?(yes/no) ")
if upload:
	execute("cd {}&&git add .".format(selected_repository_dir))
	message=input("Please enter a message for the upload: ")
	try:
		execute("cd {}&&git commit -m '{}'".format(selected_repository_dir,message))
	except:
		pass
	execute("cd {}&&git push".format(selected_repository_dir))
with open(properties_file, 'w') as configfile:    # save
	config.write(configfile)