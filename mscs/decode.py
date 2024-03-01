#!/usr/bin/env python3
# Created by Master on 4/6/2023 at 5:59 AM

import io
import struct

import mscs


def decode_message(bytesio_mscs: io.BytesIO):
    buffer = io.BytesIO(b'\x25')
    read_byte = bytesio_mscs.read(1)
    while read_byte != b',':
        buffer.write(read_byte)
        read_byte = bytesio_mscs.read(1)
        continue
    if bytesio_mscs.read(1) == b'\x00':  # 7D <00>
        pass
    breakpoint()
    return


def decode(bytesio_mscs: io.BytesIO, eof: int):
    while bytesio_mscs.tell() < eof:
        debug = bytesio_mscs.tell()  # TODO Delete
        read_byte = bytesio_mscs.read(1)
        peek = bytesio_mscs.read(1)
        bytesio_mscs.seek(-1, io.SEEK_CUR)

        if read_byte == b'\x25':  # Start message
            decode_message(bytesio_mscs)
            pass
        elif read_byte == b'\x7D':
            if peek == b'\x00':  # Stop message
                bytesio_mscs.seek(1, io.SEEK_CUR)
                pass
            pass
        elif read_byte == b'\x2C':
            if peek == b'\x00':  # End line
                bytesio_mscs.seek(1, io.SEEK_CUR)
                pass
            pass

        continue
    return
