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
