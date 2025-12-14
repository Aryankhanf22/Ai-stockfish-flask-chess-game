from flask import Flask, render_template, request, jsonify
import chess
import chess.engine
import os

app = Flask(__name__)

STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/bin/stockfish")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move")
def get_move():
    fen = request.args.get("fen")
    depth = int(request.args.get("depth", 12))

    if not fen:
        return jsonify({"error": "FEN is required"}), 400

    try:
        board = chess.Board(fen)

        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(depth=depth))

        return jsonify({
            "move": result.move.uci()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/test/<string:value>")
def test(value):
    return value
