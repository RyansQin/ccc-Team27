# vue-cli

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```

## docker build -t vuejs:V2.0.0 . (or docker pull rickylove/comp90024:vue)
use the nginx+docjer to deploy the vuejs project(before this operation, npm run build must be done)

## docker run --name vuejs -p 80:80 -d {imageId}
run the container

For detailed explanation on how things work, consult the [docs for vue-loader](http://vuejs.github.io/vue-loader).
