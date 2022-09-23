from typing import Optional, Tuple
from hex_utils import dec2hex, hex2dec
import urllib.request
import json

ADDRESS_CHARS = 40 # 160 bits
ADDRESS_OFFSET = 0
INDEX_CHARS = 14 # 56 bits
INDEX_OFFSET = ADDRESS_OFFSET + ADDRESS_CHARS
SUPPLY_CHARS = 10 # 40 bits
SUPPLY_OFFSET = INDEX_OFFSET + INDEX_CHARS

METADATA_BASE_URL = "https://api.swappable.io/api/v1/metadata/0xF20B2647679D32FF36dCD17Fe4FfA5661EF79E7b/"

def hex2dec(hex: str) -> int:
    return int(hex, 16)

def dec2hex(dec: int, length: int) -> str:
    return hex(dec)[2:].zfill(length)

def decode_swappable_id(swappable_id: int) -> Tuple[int, int, int]:
    hex_str: str = hex(swappable_id)[2:] # skip the 0x
    address: int = hex2dec(hex_str[ADDRESS_OFFSET : ADDRESS_OFFSET + ADDRESS_CHARS])
    index: int = hex2dec(hex_str[INDEX_OFFSET : INDEX_OFFSET + INDEX_CHARS])
    supply: int = hex2dec(hex_str[SUPPLY_OFFSET : SUPPLY_OFFSET + SUPPLY_CHARS])

    return address, index, supply

def encode_swappable_id(address: int, index: int, supply: int) -> int:
    addr_hex = dec2hex(address, ADDRESS_CHARS)
    idx_hex = dec2hex(index, INDEX_CHARS)
    supply_hex = dec2hex(supply, SUPPLY_CHARS)

    return hex2dec(addr_hex + idx_hex + supply_hex)

def fetch_metadata(swappable_id: int) -> Optional[object]:
    req = urllib.request.Request(
        METADATA_BASE_URL + str(swappable_id),
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    try:
        contents = urllib.request.urlopen(req).read()
        # contents = urllib.request.urlopen(METADATA_BASE_URL + str(swappable_id)).read()
        return json.loads(contents)
    except urllib.error.HTTPError:
        return None