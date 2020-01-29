import hashlib
import sys

from const import PRIVATE_CALL_OCTETS, PRIVATE_CALL, GROUP_CALL, GROUP_CALL_OCTETS


def cp_hash(inpt: str, octets: int, fmt: str = "hex"):
    b = bytes(inpt.encode())
    s = hashlib.shake_256()
    s.update(b)
    output = s.hexdigest(octets)
    if fmt == "int":
        d = s.digest(octets)
        output = int.from_bytes(d, sys.byteorder)
    return output


def gen_id(name, data) -> dict:
    if 'type' in data:
        if data['type'] == PRIVATE_CALL:
            data['id'] = cp_hash(name, PRIVATE_CALL_OCTETS, "int")
        elif data['type'] == GROUP_CALL:
            data['id'] = cp_hash(name, GROUP_CALL_OCTETS, "int")
            if data['id'] == 255:
                print(f"ERROR: Cannot use 255 for Group Call \"{name}\" unless All Call")
        elif data['type'] is None:
            data['id'] = None
        else:
            print(f"ERROR: unknown type for {name}: {data['type']}")
    else:
        data['id'] = None
    return data
