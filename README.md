# CCC Group27
## Team members:
### Shuyu Yuan - 985441
### Tai Qin - 
### Xinkai Luo - 
### Yuting Cai - 
### Renjie Zhong - 

# Vedio Links:
## Ansible

## Frontend Presentation

# Project Structure
## Frontend

## Backend

## Spider

## NLP

## Database

# Server Structure
## Instance1
### IP: 172.26.131.203
        docker container:
        1. vue: function-> frontend, ports-> 80:80
        2. proxy: function-> proxy, ports-> 8000:80 
        3. couchdb: function-> database, ports-> 4369:4369, 5984:5984, 9100-9200:9100-9200

### IP: 172.26.128.171
        Database
        Webserver
        
### IP: 172.26.130.16
        Database
        Webserver
        
### IP: 172.26.133.41
        Crawler
        NLP



# Vuejs:

## npm install
install dependencies

## npm run dev
run the server locally

## npm run build
build the static dict direcoty

## docker build -t vuejs:V2.0.0 .
use the nginx+docjer to deploy the vuejs project(before this operation, npm run build must be done)

## docker run --name vuejs -p 80:80 -d {imageId}
run the container
