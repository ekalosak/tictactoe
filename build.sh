#!/bin/bash
echo "#### START"
if [ "$(docker images -q tictactoe/base)" == "" ]; then
docker build . --file Base.Dockerfile \
  -t tictactoe/base
fi
docker build . --file App.Dockerfile \
-t tictactoe/app
echo "#### END"
