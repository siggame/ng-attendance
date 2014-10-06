# Framework libraries
from flask import Flask, render_template, request
from sqlalchemy import exc

# Local libraries
from database import Attendance, DeveloperInfo, db_session, init_db
from spreadsheet import load_roster

# Python libraries
import argparse
import json


app = Flask(__name__)


def error(msg, code=400):
    data = json.dumps({'msg': msg, 'error': code})
    return data, code


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
    if request.method == 'GET':
        return json.dumps([x.to_dict() for x in DeveloperInfo.all()])

    # It must be a POST
    try:
        data = request.get_json() or request.values
        dev = DeveloperInfo.from_dict(data)
        Attendance.mark(dev, here=True).to_json()
        return dev.to_json()
    except exc.IntegrityError, e:
        return error(e.message)


@app.route("/devs/<dev_id>", methods=['GET', 'PUT'])
def dev_detail(dev_id):
    dev = DeveloperInfo.get(dev_id)
    if not dev:
        return json.dumps(None)

    if request.method == 'GET':
        return dev.to_json()

    # It must be a PUT
    dev.update(request.get_json() or request.values)
    try:
        db_session.commit()
        return dev.to_json()
    except exc.IntegrityError, e:
        return error(e.message)


@app.route("/attendance/<dev_id>", methods=['GET', 'PUT'])
def attendance_detail(dev_id):
    dev = DeveloperInfo.get(dev_id)
    latest = Attendance.latest_for(dev)
    if not dev:
        return json.dumps(None)

    if request.method == 'GET':
        return latest.to_json()

    # It must be a PUT
    here = (request.get_json() or request.values).get('here', True)
    try:
        return Attendance.mark(dev, here=here).to_json()
    except exc.IntegrityError, e:
        return error(e.message)


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
