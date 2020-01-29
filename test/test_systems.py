import json
import os
import unittest

from const import GROUP_CALL, PRIVATE_ID_MAX, PRIVATE_CALL, GROUP_ID_MAX, SYSTEM_DIR, CONTACT_TYPES
from util import gen_id


class TestSystems(unittest.TestCase):

    def setUp(self):
        self.systems = []
        systems = [f for f in os.listdir(SYSTEM_DIR) if os.path.isfile(os.path.join(SYSTEM_DIR, f))]
        for system in systems:
            with open(os.path.join(SYSTEM_DIR, system)) as json_file:
                try:
                    self.systems.append(json.load(json_file))
                except json.decoder.JSONDecodeError:
                    self.fail(f"Problem with system file: {system}")

    def test_systems_loaded(self):
        self.assertGreater(len(self.systems), 0)

    def check_range(self, type, max):
        for system in self.systems:
            for contact in system['contacts']:
                c = system['contacts'][contact]
                if 'id' in c and c['type'] == type:
                    self.assertGreaterEqual(c['id'], 1)
                    self.assertLessEqual(c['id'], max)

    def test_private_id(self):
        self.check_range(PRIVATE_CALL, PRIVATE_ID_MAX)

    def test_group_id(self):
        self.check_range(GROUP_CALL, GROUP_ID_MAX)

    def test_duplicate_id(self):
        id_list = []
        for system in self.systems:
            for contact in system['contacts']:
                if 'id' in system['contacts'][contact]:
                    id = system['contacts'][contact]['id']
                else:
                    id = gen_id(contact, system['contacts'][contact])['id']
                if id:
                    id_list.append(id)

        self.assertEqual(len(id_list), len(set(id_list)), "System does not have unique IDs!")

    def test_type(self):
        for system in self.systems:
            for contact in system['contacts']:
                if 'type' in system['contacts'][contact]:
                    type = system['contacts'][contact]['type']
                    if type not in CONTACT_TYPES:
                        self.fail(f"{system['name']} {contact} unsupported type: {type}")

    def test_contact_channel_sites(self):
        for system in self.systems:
            for contact in system['contacts']:
                if 'channel' in system['contacts'][contact]:
                    for site_id in system['contacts'][contact]['channel']['sites']:
                        if site_id != 0 and str(site_id) not in system['sites'].keys():
                            self.fail(f"Site ID {site_id} not in {system['sites'].keys()}")

    def test_system_name(self):
        for system in self.systems:
            if 'name' not in system:
                self.fail(f"No 'name' in system {system}")

    def test_system_type(self):
        for system in self.systems:
            if 'type' not in system:
                self.fail(f"No 'type' in system {system}")

    def test_system_sites(self):
        for system in self.systems:
            if 'sites' not in system:
                self.fail(f"No 'sites' in system {system}")

    def test_system_contacts(self):
        for system in self.systems:
            if 'contacts' not in system:
                self.fail(f"No 'contacts' in system {system}")


if __name__ == '__main__':
    unittest.main()
