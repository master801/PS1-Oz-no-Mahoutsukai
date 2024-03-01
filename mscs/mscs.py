#!/usr/bin/env python3
# Created by Master on 4/5/2023 at 6:11 PM CDT

import argparse
import glob
import os
import io

import decode
import encode

# 0x04-0x137
MAGIC: bytes =                 b'\x00\x00\x01\x31\x00\x00\x00\x08\x01\x11\x02\x11' \
        b'\x11\x01\x11\x02\x11\x11\x01\x11\x01\x11\x02\x11\x11\x02\x11\x11' \
        b'\x01\x11\x02\x11\x11\x02\x11\x11\x01\x11\x01\x11\x02\x11\x20\x03' \
        b'\x11\x11\x20\x03\x11\x11\x20\x02\x11\x20\x03\x11\x11\x20\x03\x11' \
        b'\x11\x20\x05\x11\x11\x11\x20\x20\x05\x11\x11\x11\x20\x20\x02\x11' \
        b'\x11\x02\x11\x11\x01\x11\x03\x11\x11\x11\x04\x11\x11\x11\x11\x02' \
        b'\x11\x20\x01\x11\x02\x11\x20\x02\x11\x11\x01\x11\x02\x11\x11\x02' \
        b'\x11\x20\x04\x11\x11\x11\x11\x04\x11\x11\x20\x11\x02\x11\x11\x01' \
        b'\x11\x01\x11\x01\x11\x01\x11\x03\x11\x11\x11\x01\x11\x01\x11\x01' \
        b'\x11\x01\x11\x01\x11\x02\x11\x11\x02\x11\x11\x03\x11\x11\x11\x04' \
        b'\x11\x11\x11\x11\x06\x11\x11\x11\x11\x11\x11\x06\x11\x11\x11\x11' \
        b'\x11\x11\x03\x11\x11\x11\x01\x11\x02\x11\x11\x01\x11\x01\x11\x02' \
        b'\x11\x11\x02\x11\x11\x02\x11\x11\x03\x11\x11\x11\x03\x11\x11\x11' \
        b'\x04\x11\x11\x11\x11\x01\x11\x03\x11\x11\x11\x03\x11\x11\x11\x03' \
        b'\x11\x11\x11\x03\x11\x11\x11\x02\x11\x11\x02\x11\x11\x03\x11\x11' \
        b'\x20\x04\x11\x11\x20\x11\x05\x11\x11\x11\x11\x11\x05\x11\x11\x11' \
        b'\x11\x11\x02\x11\x11\x02\x11\x11\x01\x11\x02\x11\x11\x02\x11\x11' \
        b'\x08\x11\x11\x11\x11\x11\x11\x21\x21\x08\x11\x11\x11\x11\x11\x11' \
        b'\x21\x21\x01\x11\x01\x11\x03\x11\x11\x11\x01\x11\x04\x11\x11\x11' \
        b'\x21\x03\x11\x11\x11\x21\x00\x00'


def read_mscs_file(fp: str):
    print(f'Reading mscs file \"{fp}\"')

    bytesio_mscs: io.BytesIO = None
    with open(fp, mode='rb+') as io_mscs:
        bytesio_mscs = io.BytesIO(io_mscs.read())
        pass

    eof: int = bytesio_mscs.seek(-1, io.SEEK_END)

    bytesio_mscs.seek(0x04)
    if bytesio_mscs.read(len(MAGIC)) != MAGIC:
        print(f'File \"{fp}\" did not pass MAGIC test!')
        return
    else:
        print('Passed magic')
        pass

    bytesio_mscs.seek(0x1232)  # TODO DEBUG REMOVE
    decode.decode(bytesio_mscs, eof)
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', dest='input', required=True, nargs=1, type=str)
    # arg_parser.add_argument('--output', dest='output', required=True, nargs=1, type=str)  # TODO
    args = arg_parser.parse_args()

    if os.path.exists(args.input[0]):
        if os.path.isfile(args.input[0]):
            read_mscs_file(args.input[0])
            pass
        elif os.path.isdir(args.input[0]):
            found_files = glob.glob('*', root_dir=args.input[0])
            if found_files == None:
                print('Found no files!')
                return
            else:
                print(f'Found {len(found_files)} files')
                pass

            for i in found_files:
                read_mscs_file(f'{args.input[0]}{os.path.sep}{i}')
                continue
            pass
        pass
    return


if __name__ == '__main__':
    main()
    pass
