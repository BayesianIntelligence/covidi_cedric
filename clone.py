import git
import os
import sys
import shutil

GIT_REPO = 'https://gitlab.erc.monash.edu.au/stevenm/covid-intelligence-iddo/'
IMPORT_FOLDER = './covid-intelligence-iddo/'

#clone validation scripts from gitlab
def clone():
    #dir = os.listdir(IMPORT_FOLDER)
    if not os.path.exists(IMPORT_FOLDER):
        print("cloning repo...")
        git.Repo.clone_from(GIT_REPO, IMPORT_FOLDER)
    else:
        print("Repo exists - skipping clone")

    print("copying validation script into repo folder")
	
    shutil.copy("validation.py", IMPORT_FOLDER + "validation_copy.py")
    print("setting working directory to: ", IMPORT_FOLDER)
	
    os.chdir(IMPORT_FOLDER)
	
if __name__ == '__main__':
    clone()	