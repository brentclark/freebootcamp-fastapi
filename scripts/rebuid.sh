#!/bin/bash
#
# Disallow unstaged changes in the working tree
  if ! git diff-files --quiet --ignore-submodules --
  then
      echo >&2 "cannot $1: you have unstaged changes."
      git diff-files --name-status -r --ignore-submodules -- >&2
      err=1
  fi
  if [ $err = 1 ]
    then
        echo >&2 "Please commit or stash them."
        exit 1
  fi
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app stop api
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app rm -f api
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app build api --build --force-recreate --no-cache
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app create api --build --force-recreate 
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app build --no-cache api
docker compose -f docker-compose.yml -p my-freebootcamp-fastapi-app up -d --force-recreate --no-deps --build api
