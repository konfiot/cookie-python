from reedsolo import RSCodec
import json

CONF_FILE = "conf.json"

def trame(data):
    conf = json.load(open(CONF_FILE, "r"))

    out = bytearray([0xFF])
    for i, val in enumerate(data): # Concaténation des valeurs des capteurs
        out += val.to_bytes(conf["sensors"][i]["length"], byteorder='big', signed=conf["sensors"][i]["signed"])
    cs = 0

    for b in out: # Ajout du checksum XOR
        cs ^= b
    out += cs.to_bytes(1, byteorder="big", signed = False)

    rs = RSCodec(20)
    out = rs.encode(out)

    return out


