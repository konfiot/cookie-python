# -*- coding: utf-8 -*-

from reedsolo import RSCodec
import json
import operator
import struct


def trame(data, conf):
    out = bytearray([conf["trame"]["startbyte"]])

    for i, val in enumerate(data): # Concaténation des valeurs des capteurs
        out += struct.pack("!"+ conf["sensors"][i], val)

    out += bytearray([reduce(operator.xor, out)])

    rs = RSCodec(conf["trame"]["ecc"]["length"])
    out = rs.encode(out)

    return out

