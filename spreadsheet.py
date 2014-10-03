from database import DeveloperInfo

import csv
import re


def get_names(full_name):
    match = re.match(r'(\w+) ([\w ]+)', full_name)
    if match is None:
        return None
    return match.group(1), match.group(2)

def load_roster(db_session, csv_file):
    spreadsheet = csv.DictReader(csv_file)
    devs = []
    for row in spreadsheet:
        # Try to get the dev, if we already have them in the database
        d = db_session.query(DeveloperInfo).filter(DeveloperInfo.email==row['Email']).first()
        if d is None:
            d = DeveloperInfo()
            d.id = max([DeveloperInfo.next_id()] + [x.id + 1 for x in devs])

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

        devs.append(d)

    return devs
