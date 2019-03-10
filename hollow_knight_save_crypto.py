import argparse
from Crypto.Cipher import AES
import base64
import json

# provided by: https://github.com/KayDeeTee/Hollow-Knight-SaveManager/
c_sharp_header = bytes.fromhex('0001000000FFFFFFFF01000000000000000601000000')
end_header = bytes([11])
aes_key = b'UKu52ePUBwetZ9wNX88o54dnfKRu0T1l'


def read_binary_file(file_path: str):
    with open(file_path, 'rb') as binary_file:
        data = binary_file.read()
    return data


def read_json_file(file_path: str):
    with open(file_path, 'r') as text_file:
        data = json.load(text_file)
    return data


def write_data_to_file(file_path: str, bytes_):
    dict_ = json.loads(bytes_)
    str_to_write = json.dumps(dict_, indent=2, sort_keys=False)
    with open(file_path, 'w') as f:
        f.write(str_to_write)


def write_save_file(file_path: str, bytes_):
    with open(file_path, 'wb') as f:
        f.write(bytes_)


def create_cipher():
    return AES.new(aes_key, AES.MODE_ECB)


def decode_and_decrypt(bytes_):
    # remove header and last byte
    bytes_ = bytes_[len(c_sharp_header): len(bytes_) - 1]
    # decode the base64 bytes
    bytes_ = base64.b64decode(bytes_)
    # create a aes ecb-mode cipher
    cipher = create_cipher()
    # decrypt
    bytes_ = cipher.decrypt(bytes_)
    # finally remove padding
    return bytes_[:-bytes_[-1]]


def encrypt_and_encode(bytes_):
    # create a aes ecb-mode cipher
    cipher = create_cipher()
    # add padding
    length = 16 - (len(bytes_) % 16)
    bytes_ += bytes([length]) * length
    # encrypt
    bytes_ = cipher.encrypt(bytes_)
    # encode to base64
    bytes_ = base64.b64encode(bytes_)
    # add static header, length header and final byte
    bytes_ = c_sharp_header + c_sharp_length(bytes_) + bytes_ + end_header
    return bytes_


def c_sharp_length(bytes_):
    bytes_len = len(bytes_)
    values = []
    for i in range(4):
        if bytes_len >> 7 == 0:
            values.append(0x7F & bytes_len)
            bytes_len = bytes_len >> 7
            break
        else:
            values.append(0x7F & bytes_len | 0x80)
            bytes_len = bytes_len >> 7
    if bytes_len != 0:
        values.append(bytes_len)
    return bytes(values)


def decrypt_handle(args):
    if args.output is None:
        if len(args.input.split('.')) > 0:
            alt_file_out = '.'.join(args.input.split('.')) + '.json'
        else:
            alt_file_out = args.input + '.json'
        if args.verbose:
            print(f'no output file name provided. will output to "{alt_file_out}"')
    if args.verbose:
        print('decrypt mode')
        print()
        print(f'reading file: {args.input}')
    data_as_bytes = read_binary_file(args.input)
    if args.verbose:
        print('decrypting... ', end='')
    data_as_bytes = decode_and_decrypt(data_as_bytes)
    if args.verbose:
        print('ok')
        print(f'writing to file: {args.output or alt_file_out})')
    write_data_to_file(args.output or alt_file_out, data_as_bytes)
    if args.verbose:
        print('done')


def encrypt_handle(args):
    if args.output is None:
        if len(args.input.split('.')) > 0:
            alt_file_out = '.'.join(args.input.split('.')) + '.dat'
        else:
            alt_file_out = args.input + '.dat'
        if args.verbose:
            print(f'no output file name provided. will output to "{alt_file_out}"')
    if args.verbose:
        print('encrypt mode')
        print()
        print(f'reading file: {args.input}')
    dict_ = read_json_file(args.input)
    # restructure data: json/dict -> string
    str_ = json.dumps(dict_, separators=[',', ':'])
    # restructure data: string -> bytes
    data_as_bytes = bytes(str_, encoding='utf-8')
    if args.verbose:
        print('encrypting... ', end='')
    data_as_bytes = encrypt_and_encode(data_as_bytes)
    if args.verbose:
        print('ok')
        print(f'writing to file: {args.output or alt_file_out})')
    write_save_file(args.output or alt_file_out, data_as_bytes)
    if args.verbose:
        print('done')


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.required = True
    decrypt_sp = subparsers.add_parser('decrypt', help='decrypt a hollow knight save file (.dat) and output it to terminal or a json-file (.json)')
    encrypt_sp = subparsers.add_parser('encrypt', help='encrypt a json-file (.json) to a hollow knight save file (.dat)')
    decrypt_sp.set_defaults(func=decrypt_handle)
    encrypt_sp.set_defaults(func=encrypt_handle)
    decrypt_required_named = decrypt_sp.add_argument_group('required named arguments')
    decrypt_required_named.add_argument('-i', '--input', type=str, help="hollow knight save file (.dat) to decrypt", required=True)
    decrypt_sp.add_argument('-o', '--output', type=str, help="file to output the content of the hollow knight save file")
    decrypt_sp.add_argument('-v', '--verbose', action='store_true', help="verbose output")
    encrypt_required_named = encrypt_sp.add_argument_group('required named arguments')
    encrypt_required_named.add_argument('-i', '--input', type=str, help="hollow knight save file in json-format (.json)", required=True)
    encrypt_sp.add_argument('-o', '--output', type=str, help="file to output hollow knight save data")
    encrypt_sp.add_argument('-v', '--verbose', action='store_true', help="verbose output")
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
