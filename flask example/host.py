from flask import Flask, render_template, jsonify, request
from go_matt import *

app = Flask(__name__, template_folder="templates", static_folder="static")
G = Game()


@app.route("/")
def index():
    G = Game()
    return render_template("index.html")


@app.route('/test_fxn')
def test_fxn():
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        color = request.args.get('color')
        G.play((y, x), color)
        print(render_board(G.board, '.'))
        print(G.rules)
        print(G.captures)
        print(G.latest_status)
        return jsonify(result=("x=", x, "y=", y, color))
    except Exception as e:
        print(str(e))
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
