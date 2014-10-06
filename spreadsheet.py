from database import DeveloperInfo

import csv
import re
import StringIO


def get_names(full_name):
    match = re.match(r'(\w+) ([\w ]+)', full_name)
    if match is None:
        return None
    return match.group(1), match.group(2)

def load_roster(db_session, csv_file):
    spreadsheet = csv.DictReader(csv_file)
    for row in spreadsheet:
        # Try to get the dev, if we already have them in the database
        d = db_session.query(DeveloperInfo).filter(DeveloperInfo.email==row['Email']).first()
        if d is None:
            d = DeveloperInfo()
            d.id = DeveloperInfo.next_id()

        # Try to split the name into first/last
        names = get_names(row['Full'])
        if names is None:
            print '\tUnable to split name "{}"'.format(row['Full'])
            continue

        d.first_name, d.last_name = names
        d.preferred_name=row['Preferred']
        d.email=row['Email']
        d.github_username=row['Username']
        d.team=row['Team']
        d.planning_to_compete=row['Wants to Compete'] == "Yep"
        d.added_manually = False

        db_session.add(d)
        db_session.commit()


def dump_roster(db_session):
    devs = db_session.query(DeveloperInfo).all()
    fields = [col.name for col in DeveloperInfo.__table__.columns]
    fields.append('here')

    csv_strfile = StringIO.StringIO()
    writer = csv.DictWriter(csv_strfile, fieldnames=fields)
    writer.writerow({f: f for f in fields})
    for dev in devs:
        writer.writerow(dev.to_dict())

    print csv_strfile.getvalue()



if __name__ == '__main__':
    from database import db_session
    dump_roster(db_session)
