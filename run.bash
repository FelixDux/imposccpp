#!/bin/bash

SOURCE_DIR=$(realpath "$0" |xargs dirname)

function image_count {
    docker images |grep -w -c $1
}

function build_image {
    cd $SOURCE_DIR/$1; image_count $1 && echo $1 exists || docker build --no-cache -t $1:latest .; cd -;
}

function run_image {
    docker run -p $2:$3 --rm $1:latest &
}

build_image imposc-service

build_image imposc-ui

run_image imposc-service 5000 5000

run_image imposc-ui 3000 80

echo "Front-end can be accessed from http://localhost:3000"
