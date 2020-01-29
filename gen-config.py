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

        print(f"# {data['name']}")
        print()
        print(f"System type: {data['type']}")
        print(f"System code: {data['code']}")
        print()

        print("## Contacts")
        print()
        print("Name             | Type         | ID")
        print("---------------- | ------------ | -----")
        rows = []
        ic = 0
        for name in data['contacts']:
            contact = data['contacts'][name]
            if 'publish' in contact and contact['publish']:
                rows.append(
                    f"{name:16} | {contact['type']:12} | {contact['id']:5}")
                ic += 1
        for r in sorted(rows):
            print(r)

        print()
        print("## Radio IDs")
        print()
        print("Name             | ID")
        print("---------------- | -----")
        rows = []
        ir = 0
        for name in data['contacts']:
            contact = data['contacts'][name]
            if 'type' in contact and contact['type'] == PRIVATE_CALL:
                rows.append(
                    f"{name:16} | {contact['id']:5}")
                ir += 1
        for r in sorted(rows):
            print(r)

        print()
        print("## Channels")
        print()
        print("Name")
        print("----------------")
        iz = 0
        for name in data['contacts']:
            contact = data['contacts'][name]
            if 'channel' in contact:
                print(f"{name:16}")
                iz += 1

        print()
        print(f"{ic} contacts")
        print(f"{ir} radios")
        print(f"{iz} channels")

        print()
        print("----")
        print()
