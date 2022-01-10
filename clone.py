import git
import os
import sys
import shutil

GIT_REPO = 'https://gitlab.erc.monash.edu.au/stevenm/covid-intelligence-iddo/'
# using temporary GIT repo replacement, SWSLHD does not have access to gitlab
#GIT_REPO = "https://github.com/COVID-I/covidi_validation"
IMPORT_FOLDER = './covid-intelligence-iddo/'
# using tremporay git repo replacement
#IMPORT_FOLDER = './covidi_validation/'

#clone validation scripts from gitlab
def clone():
    #dir = os.listdir(IMPORT_FOLDER)
    if not os.path.exists(IMPORT_FOLDER):
        print("cloning repo...")
        git.Repo.clone_from(GIT_REPO, IMPORT_FOLDER)
    else:
        print("Repo exists - skipping clone")

    print("copying validation script into repo folder")
	
    shutil.copy("validation.py", IMPORT_FOLDER + "validation.py")
    print("setting working directory to: ", IMPORT_FOLDER)
	
    os.chdir(IMPORT_FOLDER)
	
if __name__ == '__main__':
    clone()	