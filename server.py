from flask import Flask
from flask import render_template
from flask import request

import argparse
import names
import json

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("names_list.html")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("names",
                      type=file,
                      help="JSON file with a list of names")
  args = parser.parse_args()

  with args.names as names_file:
    names = json.load(names_file)
    names_list = list(names)

  app.run(debug=True)
