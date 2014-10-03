# Framework libraries
from flask import Flask, render_template, request

# Local libraries
from database import DeveloperInfo, db_session, init_db
from spreadsheet import load_roster

# Python libraries
import argparse
import json


app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET'])
def index():
    return render_template('attendance.html')


@app.route("/teams", methods=['GET'])
def teams_list():
    teams = ['Arena', 'Server/Client', 'Testing', 'Visualizer', 'Web']
    return json.dumps(teams)


@app.route("/devs", methods=['GET', 'POST'])
def dev_list():
    return json.dumps([x.to_dict() for x in DeveloperInfo.all()])


@app.route("/devs/<dev_id>", methods=['GET', 'PUT'])
def dev_detail(dev_id):
    dev = DeveloperInfo.get(dev_id)
    if dev:
        return dev.to_json()
    return json.dumps(None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("roster",
                        nargs='?',
                        type=file,
                        help="Tab-separated spreadsheet of people")
    args = parser.parse_args()

    init_db()

    if args.roster:
        print "Populating database using spreadsheet..."
        load_roster(db_session, args.roster)
        print "\tDone"

    app.run(debug=True)
