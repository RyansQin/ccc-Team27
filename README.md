# CCC Group27
## Team members:
### Shuyu Yuan - 985441
### Tai Qin - 1005309
### Xinkai Luo - 
### Yuting Cai - 982332
### Renjie Zhong - 961201

# Vedio Links:
## Ansible

## Frontend Presentation

# Project Structure
## Frontend
### In this project, vuejs is chose to be the front end of our application. Vue is a single page application that enables partial refresh of the page without requesting all data and dom every time you jump to the page, which greatly improve the access speed and the user experience. Different components represents differenty functionality, which makes the developer design more easily. And its third-party ui library, like bootstrap, font-awesome-icon, etc., saves a lot of development time. As for the data, central storage is used to manage the global data of different part.

## Backend

## Spider

## NLP

### Topic Clustring

        Use `LDA (Latent Dirichlet Allocation)` for topic clustering. `LDA` uses the common features of the terms in the text to discover the topic of the text and does not require any background knowledge about the text.

### Sentiment Analysis

        We used the `TextBlob` library to perform sentiment analysis on the tweets we crawled. `TextBlob` is a python library which provides a simple API for NLP task.

## Database

# Server Structure
## Instance1
### IP: 172.26.131.203
        docker container:
        1. vue: function-> frontend, ports-> 80:80
        2. proxy: function-> proxy, ports-> 8000:80 
        3. couchdb: function-> database, ports-> 4369:4369, 5984:5984, 9100-9200:9100-9200

## Instance2
### IP: 172.26.128.171
        docker container:
        1. flask: function-> backend, ports-> 8080:5000
        2. couchdb: function-> database, ports-> 4369:4369, 5984:5984, 9100-9200:9100-9200
        
## Instance3
### IP: 172.26.130.16
        docker container:
        1. flask: function-> backend, ports-> 8080:5000
        2. couchdb: function-> database, ports-> 4369:4369, 5984:5984, 9100-9200:9100-9200
        
## Instance4
### IP: 172.26.133.41
        docker container:
        1. crawler: function-> crawler
        2. nlp: function-> nlp



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
