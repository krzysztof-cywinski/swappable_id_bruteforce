def hex2dec(hex: str) -> int:
    return int(hex, 16)

def dec2hex(dec: int, length: int) -> str:
    return hex(dec)[2:].zfill(length)