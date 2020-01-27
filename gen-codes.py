import json
import os

from const import CODE_OCTETS, SYSTEM_DIR, GROUP_CALL
from util import cp_hash, gen_id

systems = [f for f in os.listdir(SYSTEM_DIR) if os.path.isfile(os.path.join(SYSTEM_DIR, f))]

for system in systems:
    with open(os.path.join(SYSTEM_DIR, system)) as json_file:
        data = json.load(json_file)

        for contact in data['contacts']:
            c = data['contacts'][contact]

            if 'id' not in c:
                gen_id(contact, c)

            if 'code' not in c \
                    and 'channel' in c and c['channel']:
                c['code'] = cp_hash(contact, CODE_OCTETS)

        print(f"# {data['name']}\n")
        print(f"System type: {data['type']}\n")

        print("## Contacts\n")
        print("Name             | Type         | ID    | Code")
        print("---------------- | ------------ | ----- | ----------")
        rows = []
        for name in data['contacts']:
            contacts = data['contacts']
            contact = contacts[name]
            if 'publish' in contact and contact['publish']:
                rows.append(
                    f"{name:16} | {contact['type']:12} | {contact['id']:5} | {contact['code'] if 'code' in contact else ''}")
        for r in sorted(rows):
            print(r)

        print("\n## Radio IDs\n")
        print("Name             | ID")
        print("---------------- | -----")
        rows = []
        for name in data['contacts']:
            contacts = data['contacts']
            contact = contacts[name]
            if contact['type'] == "Private Call":
                rows.append(
                    f"{name:16} | {contact['id']:5}")
        for r in sorted(rows):
            print(r)

        print("\n## Channels\n")
        print("No. | Name")
        print("--- | ----------------")
        i = 1
        for name in data['contacts']:
            contacts = data['contacts']
            contact = contacts[name]
            if 'channel' in contact and contact['channel'] \
                    and 'publish' in contact and contact['publish']:
                print(
                    f"{i:3} | {name}")
                i += 1

        print("\n----\n")
