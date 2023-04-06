#!/usr/bin/env python3

# File: bin.py
# Created by: Master
# Date: 9/23/2022 at 9:44 PM CDT

import argparse
import io
import os
import struct
import dataclasses
import glob

MAGIC: bytes = b'JOIN'

MAP_FILES: dict[{str: dict[{int, str}]}] = {
    'MSCS.BIN': {
        0: None,
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
        11: None,
        12: None,
        13: None,
        14: None,
        15: None,
        16: None,
        17: None,
        18: None,
        19: None,
        20: None,
        21: None,
        22: None,
        23: None,
        24: None,
        25: None,
        26: None,
        27: None,
        28: None,
        29: None,
        30: None,
        31: None,
        32: None,
        33: None,
        34: None,
        35: 'INTRO.MSCS',
        36: None,
        37: None,
        38: None,
        39: None,
        40: None,
        41: None,
        42: None,
        43: None,
        44: None,
        45: None,
        46: None,
        47: None,
        48: None,
        49: None,
        50: None,
        51: None,
        52: None,
        53: None,
        54: None,
        55: None,
        56: None,
        57: None,
        58: None,
        59: None,
        60: None,
        61: None,
        62: None,
        63: None,
        64: None
    }
}


@dataclasses.dataclass
class Entry:
    offset: int
    length: int


# noinspection PyTypeChecker
def extract_bin(root_fp: str, fn: str, out_dir: str):
    if root_fp is None:
        fp = fn
        pass
    else:
        fp = os.path.join(root_fp, fn)
        pass

    entries: list[Entry] = []
    with open(fp, mode='rb+') as io_bin:
        if io_bin.read(len(MAGIC)) != MAGIC:
            print('Bad magic!')
            io_bin.close()
            return
        else:
            print(f'File \"{fp}\" passed magic check')
            pass

        entries_amnt: int = struct.unpack('<I', io_bin.read(0x4))[0]
        for i in range(entries_amnt):
            offset: int = struct.unpack('<I', io_bin.read(0x4))[0]
            length: int = struct.unpack('<I', io_bin.read(0x4))[0]
            if offset != 0x0000 and length != 0x0000:
                entries.append(
                    Entry(offset, length)
                )
                print(f'Found file entry ({offset}, {length})')
                continue
            del length
            del offset
            continue
        del entries_amnt

        print(f'\nFound {len(entries)} files\n')

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            print(f'Created extract directory \"{out_dir}\"\n')
            pass

        for i in range(len(entries)):
            entry = entries[i]
            io_bin.seek(entry.offset, io.SEEK_SET)
            header = io_bin.read(0x4)
            is_container = header == b'\x00\x00\x03\x01'

            if is_container:
                io_bin.seek(0x4, io.SEEK_CUR)
                pass
            else:
                io_bin.seek(entry.offset, io.SEEK_SET)
                pass

            is_tim = io_bin.read(0x4) == b'\x10\x00\x00\x00'
            io_bin.seek(-0x4, io.SEEK_CUR)
            is_vab = io_bin.read(0x4) == b'\x70\x42\x41\x56'

            name: str = None
            if fn in MAP_FILES:
                if i in MAP_FILES[fn]:
                    name = MAP_FILES[fn][i]
                    pass
                pass

            if name is None:
                name = str(i)
                pass
            else:
                print(f'Mapped {i} to \"{name}\"')
                pass

            if is_container:
                io_bin.seek(entry.offset, io.SEEK_SET)
                fp_header = os.path.join(out_dir, f'{name}.header')

                if os.path.exists(fp_header):
                    mode = 'wb+'
                    pass
                else:
                    mode = 'wb'
                    pass

                with open(fp_header, mode=mode) as io_entry:
                    io_entry.write(
                        io_bin.read(0x8)
                    )
                    print(f'Wrote extracted header \"{io_entry.name}\"')
                    pass
                del mode
                del fp_header
                pass

            ps = os.path.join(out_dir, name)
            if is_tim:
                ps += '.tim'
                pass
            elif is_vab:
                ps += '.vab'
                pass

            if os.path.exists(ps):
                mode = 'wb+'
                pass
            else:
                mode = 'xb'
                pass

            with open(ps, mode=mode) as io_entry:
                if is_container:
                    io_bin.seek(entry.offset + 0x8, io.SEEK_SET)
                    pass
                else:
                    io_bin.seek(entry.offset, io.SEEK_SET)
                    pass
                io_entry.write(
                    io_bin.read(entry.length)
                )
                print(f'Wrote extracted file \"{io_entry.name}\"')
                pass
            continue

        print('\nDone extracting\n')
        pass
    return


def extract_bins(_input: str, output: str):
    if os.path.isdir(_input):
        for i in glob.glob('*.BIN', root_dir=_input, recursive=False):
            print(f'Found file \"{i}\" to extract')
            if output is not None:
                output = output
                pass
            else:
                output = os.path.join(_input, i[0:i.index('.')])
                pass
            extract_bin(_input, i, output)
            continue
        pass
    elif os.path.isfile(_input):
        if output is not None:
            output = output
            pass
        else:
            output = _input[:-4]
            pass
        extract_bin(None, _input, output)
        pass
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', dest='input', required=True, nargs=1, type=str)
    arg_parser.add_argument('--output', dest='output', required=False, nargs=1, type=str)
    args = arg_parser.parse_args()

    if not os.path.exists(args.input[0]):
        print('No input file or directory specified!')
        return

    if True:
        if args.output is None:
            output = None
            pass
        else:
            output = args.output[0]
            pass
        extract_bins(args.input[0], output)
        pass

    return


if __name__ == '__main__':
    main()
    pass
