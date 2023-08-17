import base64

async def encode(string: str):
    string_bytes = string.encode("ascii")
    b64_bytes = base64.urlsafe_b64encode(string_bytes)
    b64_string = b64_bytes.decode("ascii")
    return b64_string

async def decode(string: str):
    b64_string = string
    b64_bytes = b64_string.encode("ascii")
    decoded_bytes = base64.urlsafe_b64decode(b64_bytes)
    decoded_string = decoded_bytes.decode("ascii")
    return decoded_string

async def encryt(string: str):
    pass


async def decrypt(string: str):
    pass