from flask import Flask, render_template, request
import chess
import chess.engine
import os

# Initialize Flask app
app = Flask(__name__)

# ✅ CHANGE 1: Linux-compatible Stockfish path (Railway/Docker)
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/bin/stockfish")

# ❌ REMOVE Windows-only existence check
# if not os.path.exists(STOCKFISH_PATH):
#     raise FileNotFoundError(...)


@app.route('/')
def index():
    return render_template("index.html")


# ✅ CHANGE 2: Use query params instead of path (fix FEN issue)
@app.route('/move')
def get_move():
    try:
        depth = int(request.args.get("depth", 12))
        fen = request.args.get("fen")

        if not fen:
            return "FEN missing", 400

        board = chess.Board(fen)

        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(depth=depth))
            move = result.move

        return str(move)

    except Exception as e:
        return str(e), 500


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


# ❌ REMOVE app.run() for production
# Gunicorn handles this
