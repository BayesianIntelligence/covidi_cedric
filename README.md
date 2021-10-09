# covidi_cedric README  
# deployment instructions  
#to clone the git repo to your local environment  
```
git clone https://github.com/COVID-I/covidi_cedric.git  
```
#to build the docker image and give the image the name: covidi_cedric:latest 
```
cd covidi_cedric  
sudo docker build -t covidi_cedric:latest .  
``` 
#to run the container (-d : in the background; -p 5000:5000 map the docker container port 5000 to the host port 5000)  
```
sudo docker run -d -p 5000:5000 --name covidi_cedric covidi_cedric   
```  
# how to use  
#to confirm the API is working via a web browser  
```
http://localhost:5000  
```
#to return all nodes and distributions from the BN model  
```
http://localhost:5000/getall  
```
