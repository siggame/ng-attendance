from flask import Flask
from flask import render_template
from flash import request

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("name_list.html")

if __name__ == "__main__":
  app.run(debug=True)
