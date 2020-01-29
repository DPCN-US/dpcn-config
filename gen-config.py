import json
import os

from const import CODE_OCTETS, SYSTEM_DIR, PRIVATE_CALL
from util import cp_hash, gen_id

systems = [f for f in os.listdir(SYSTEM_DIR) if os.path.isfile(os.path.join(SYSTEM_DIR, f))]

for system in systems:
    with open(os.path.join(SYSTEM_DIR, system)) as json_file:
        data = json.load(json_file)

        if 'code' not in data:
            data['code'] = cp_hash(data['name'], CODE_OCTETS)

        for contact in data['contacts']:
            c = data['contacts'][contact]

            if 'id' not in c:
                gen_id(contact, c)

        print(f"# {data['name']}\n")
        print(f"System type: {data['type']}")
        print(f"System code: {data['code']}\n")

        print("## Contacts\n")
        print("Name             | Type         | ID")
        print("---------------- | ------------ | -----")
        rows = []
        ic = 0
        for name in data['contacts']:
            contacts = data['contacts']
            contact = contacts[name]
            if 'publish' in contact and contact['publish']:
                rows.append(
                    f"{name:16} | {contact['type']:12} | {contact['id']:5}")
                ic += 1
        for r in sorted(rows):
            print(r)

        print("\n## Radio IDs\n")
        print("Name             | ID")
        print("---------------- | -----")
        rows = []
        ir = 0
        for name in data['contacts']:
            contacts = data['contacts']
            contact = contacts[name]
            if contact['type'] == PRIVATE_CALL:
                rows.append(
                    f"{name:16} | {contact['id']:5}")
                ir += 1
        for r in sorted(rows):
            print(r)

        print("\n## Channels\n")
        print("Name")
        print("----------------")
        iz = 0
        for name in data['contacts']:
            contacts = data['contacts']
            contact = contacts[name]
            if ('channel' in contact and contact['channel']) \
                    and ('publish' in contact and contact['publish'])\
                    or contact['type'] is None:
                print(
                    f"{name:16}")
                iz += 1

        print(f"\n{ic} contacts")
        print(f"{ir} radios")
        print(f"{iz} channels")

        print("\n----\n")
