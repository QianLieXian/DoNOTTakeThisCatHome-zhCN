# Sparse text-pixel changes only. Original art is read from the installed game.
init 997 python:
    import base64 as _zi_b64
    import hashlib as _zi_hash
    import io as _zi_io
    import json as _zi_json
    import os as _zi_os
    import struct as _zi_struct
    import zlib as _zi_zlib

    with open(_zi_os.path.join(config.gamedir, "zhcn_image_deltas.json"), "r", encoding="utf-8") as _zi_file:
        _zhcn_image_deltas = _zi_json.load(_zi_file)
    _zi_previous_open = config.file_open_callback

    def _zhcn_open_image(name):
        key = name.replace("\\", "/")
        if key.startswith("images/"):
            key = key[7:]
        info = _zhcn_image_deltas.get(key)
        if info is not None and _preferences.language == "zh_CN":
            if key not in _zhcn_open_image.cache:
                source = _zi_os.path.join(config.gamedir, "images", *key.split("/"))
                with open(source, "rb") as stream:
                    original = stream.read()
                if _zi_hash.sha256(original).hexdigest() != info["sha256"]:
                    renpy.log("Chinese text-image patch skipped: unsupported original " + key)
                    return None
                position = 8
                compressed = []
                while position < len(original):
                    length = _zi_struct.unpack(">I", original[position:position+4])[0]
                    kind = original[position+4:position+8]
                    payload = original[position+8:position+8+length]
                    if kind == b"IHDR":
                        ihdr = payload
                    elif kind == b"IDAT":
                        compressed.append(payload)
                    position += length + 12
                pixels = bytearray(_zi_zlib.decompress(b"".join(compressed)))
                edits = _zi_io.BytesIO(_zi_zlib.decompress(_zi_b64.b64decode(info["data"])))
                while True:
                    header = edits.read(8)
                    if not header:
                        break
                    offset, length = _zi_struct.unpack("<II", header)
                    pixels[offset:offset+length] = edits.read(length)
                def chunk(kind, payload):
                    return _zi_struct.pack(">I", len(payload)) + kind + payload + _zi_struct.pack(">I", _zi_zlib.crc32(kind + payload) & 0xffffffff)
                result = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", _zi_zlib.compress(pixels, 3)) + chunk(b"IEND", b"")
                _zhcn_open_image.cache[key] = result
            return _zi_io.BytesIO(_zhcn_open_image.cache[key])
        if _zi_previous_open is not None:
            return _zi_previous_open(name)
        return None

    _zhcn_open_image.cache = {}
    config.file_open_callback = _zhcn_open_image
