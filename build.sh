#!/bin/bash
echo "#### START"
docker build . --file Base.Dockerfile \
  -t tictactoe/base && \
  docker build . --file App.Dockerfile \
  -t tictactoe/app
echo "#### END"
