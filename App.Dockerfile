FROM tictactoe/base:latest

COPY game.py /app/
WORKDIR /app
CMD [ "python", "game.py" ]
