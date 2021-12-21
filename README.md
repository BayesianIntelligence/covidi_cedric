# covidi_cedric README  
# deployment instructions  
#to clone the git repo to your local environment  
```
git clone https://github.com/COVID-I/covidi_cedric.git  
```
# building with docker
#to build the docker image and give the image the name: covidi_cedric:latest 
```
cd covidi_cedric  
sudo docker build -t covidi_cedric:latest .  
``` 
#to run the container (-d : in the background; -p 5000:5000 map the docker container port 5000 to the host port 5000)  
```
sudo docker run -d -p 5000:5000 --name covidi_cedric -v ${pwd}/data_input:/app/data_in -v ${pwd}/data_output:/app/data_out covidi_cedric
```  
# building with docker-compose
#if it's easier I have also provided a docker-compose file that does the same thing, to build and run in one command:
```
sudo docker-compose up -d
```
#if for any reason you need to access the docker container directly you can use the following command:
```
sudo docker exec -it covidi_cedric /bin/bash
```
# how to use  
#to confirm the API is working via a web browser  
```
http://localhost:5000  
```
#to [GET] all nodes and distributions from the BN model via HTTP  
```
http://localhost:5000/getall  
```
#The API also supports POST to the same end point
```
http://localhost:5000/getall  
```
#the POST statement allows you to set evidence on the BN. Here is an example JSON body with evidence set for 2 nodes.
```
{
    "ci_age_group_bg":"adult",
    "ci_anticoag_treat_bl":"FALSE"
}
```
#any number of BN nodes can be set, the API will simply ignore incorrectly named nodes. The file "bn_node_output_file.xlsx" provides a full list of possible nodes and their states, and can be found in the same fodler as this README.

#Volume based model validation - in order to perform model validation, a JSON file must be provided via a documer volume.

# when performing this outside of docker.

# save the import JSON file to data_input as file name test_json:
cp sourcefile.json data_input/test_file.json

# create the database from the JSON file:
python db.py

# this will create a file in data_output called covidi.db NB THIS CONTAINS SOURCE DATA SO SHOULD NOT BE SHARED EXTERNALLY

# You will require all the validation scripts from GITHUB, these are stored and maintained seperately to the COVID-I-CEDRIC source code. To pull this codebase, run:
python clone.py

#copy the validation file to the newely cloned folder
cp validation.py covid-intelligence-iddo/validation.py

cd covid-intelligence-iddo

#finally, to perform the validation process, run the validation script: 
python validation.py