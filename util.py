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
        if output == 255:
            print(f"ERROR: Cannot use 255 for Group Call \"{inpt}\" unless All Call")
    return output


def gen_id(name, data) -> dict:
    if data['type'] == PRIVATE_CALL:
        data['id'] = cp_hash(name, PRIVATE_CALL_OCTETS, "int")
    elif data['type'] == GROUP_CALL:
        data['id'] = cp_hash(name, GROUP_CALL_OCTETS, "int")
    else:
        print(f"ERROR: unknown type for {data}: {data['type']}")
    return data
