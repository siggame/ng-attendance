# Framework libraries
from flask import Flask
from flask import render_template
from flask import request

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


@app.route("/")
def index():
    return render_template('attendance.html')


@app.route("/teams")
def teams_list():
    teams = ['Arena', 'Server/Client', 'Testing', 'Visualizer', 'Web']
    return json.dumps(teams)


@app.route("/devs")
def dev_list():
    return json.dumps([x.to_dict() for x in DeveloperInfo.all()])


@app.route("/devs/<dev_id>")
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
        db_session.add_all(load_roster(db_session, args.roster))
        db_session.commit()
        print "\tDone"

    app.run(debug=True)
