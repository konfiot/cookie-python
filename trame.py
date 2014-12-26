# -*- coding: utf-8 -*-

from reedsolo import RSCodec
import json
import operator
import struct

CONF_FILE = "conf.json"

def trame(data):
    conf = json.load(open(CONF_FILE, "r"))

    out = bytearray([conf["trame"]["startbyte"]])

    for i, val in enumerate(data): # Concaténation des valeurs des capteurs
        out += struct.pack("!"+ conf["sensors"][i], val)

    out += bytearray([reduce(operator.xor, out)])

    rs = RSCodec(conf["trame"]["ecc"]["length"])
    out = rs.encode(out)

    return out

