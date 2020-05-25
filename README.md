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

## Twitter harvester
### In this project, the Standard Search API provided by Twitter Developer Account is used to collect tweets data. We have collected two kinds of tweets text; each kind is classified by the state. The first kind is the exact tweet from a certain state while the other kind is any tweets that contain the keywords like ‘lockdown’, ‘stay home’, etc. In order to get the exact tweet from a certain state, we set the ‘geocode’ parameter in search API to specify the latitude and longitude of the most populated city in that state. There are two crawler programs that can automatically collect Twitter data without any omissions and duplications once opened.

## NLP

### Topic Clustring

Use `LDA (Latent Dirichlet Allocation)` for topic clustering. `LDA` uses the common features of the terms in the text to discover the topic of the text and does not require any background knowledge about the text. `LDA` will generate a topic for each term in each document. From the perspective of document clustering, `LDA` does not have a uniform clustering label for documents, but each term has a clustering label, and that is the topic. The final output of LDA is the topics, the terms of each topic and the weight of each term. The number of topics and the number of terms in each topic can be customized.

### Sentiment Analysis

We used the `TextBlob` library to perform sentiment analysis on the tweets we crawled. `TextBlob` is a python library which provides a simple API for NLP task. We used its sentiment analysis feature to analyze whether Australian tweets were positive or negative during lockdown. The result returned by `TextBlob` is a tuple, which includes polarity, subjectivity, and assessment. We can judge the emotion of the text by analyzing the obtained polarity.

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
