from flask import Flask, render_template, url_for, request, redirect, abort, flash, jsonify, session, make_response
import sqlite3
import sys
sys.path.append('..')
from utils import sqlite_utils




app = Flask(__name__)

@app.route('/')
def index():
    gainerConn = sqlite_utils.createConnection("/var/stockSA/stockGainers.db")

    multiStockGainers = sqlite_utils.findMultipleStockGainers(gainerConn)
    print(multiStockGainers)

    return render_template("index.html", graph1 = multiStockGainers)


if __name__ == "__main__":
    app.run(debug=True)
