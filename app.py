from flask import Flask, render_template
import chess
import chess.engine
import os

app = Flask(__name__)

# Linux Stockfish path (installed via apt in Dockerfile)
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/bin/stockfish")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move/<int:depth>/<path:fen>/")
def get_move(depth, fen):
    try:
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            board = chess.Board(fen)
            result = engine.play(board, chess.engine.Limit(depth=depth))
            return str(result.move)
    except Exception as e:
        return str(e), 500


@app.route("/test/<string:value>")
def test(value):
    return value
