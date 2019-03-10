# Hollow-Knight-Save-Crypto

A CLI (commandline-interface) decrypt and encrypt utility for Hollow Knight save files written in Python 3. The basic usage contains two modes:

- `decrypt`: decrypt a hollow knight save file and save the resulting data in a json-formatted text file
- `encrypt`: encrypt a json-formatted save file and save the result as a hollow knight save file

A bundled executable for Windows can be downloaded in `releases`: https://github.com/nakami/Hollow-Knight-Save-Crypto/releases

Inspired by:

- Hollow-Knight-SaveManager by KayDeeTee: https://github.com/KayDeeTee/Hollow-Knight-SaveManager/
- hollow by bloodorca: https://github.com/bloodorca/hollow

# Requirements

If you want to run the script as a bundled Windows executable, you do not need to install anything.

If you want to run the Python script via Python you need to install the following package:

```
pycryptodome
```

You can install this package by running `pip install pycryptodome`

# Usage

Shown here is the usage by running the Python script. Using the bundled Windows Executable, just replace the command `python hollow_knight_save_crypto.py` with `hollow_knight_save_crypto.exe`.

## Decrypting

- `-i FILE_PATH` or `--input FILE_PATH`: (required) path to a hollow knight save file
- `-o FILE_PATH` or `--output FILE_PATH`: path for a resulting json-formatted text file
- `-v` or `--verbose`: verbose output (outputs some details in the commandline)

```console
> python .\hollow_knight_save_crypto.py decrypt -h
usage: hollow_knight_save_crypto.py decrypt [-h] -i INPUT [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        file to output the content of the hollow knight save
                        file
  -v, --verbose         verbose output

required named arguments:
  -i INPUT, --input INPUT
                        hollow knight save file (.dat) to decrypt
```

example:

```console
> python .\hollow_knight_save_crypto.py decrypt -i user1.dat -o user1.json -v
decrypt mode

reading file: user1.dat
decrypting... ok
writing to file: user1.json)
done
```

## Encrypting

- `-i FILE_PATH` or `--input FILE_PATH`: (required) path to resulting json-formatted text file
- `-o FILE_PATH` or `--output FILE_PATH`: path for a resulting hollow knight save file
- `-v` or `--verbose`: verbose output (outputs some details in the commandline)

```console
> python .\hollow_knight_save_crypto.py encrypt -h
usage: hollow_knight_save_crypto.py encrypt [-h] -i INPUT [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        file to output hollow knight save data
  -v, --verbose         verbose output

required named arguments:
  -i INPUT, --input INPUT
                        hollow knight save file in json-format (.json)
```

example:

```console
> python .\hollow_knight_save_crypto.py encrypt -i user1.json -o newsave.dat -v
encrypt mode

reading file: user1.json
encrypting... ok
writing to file: newsave.dat)
done
```

# Contribute

Feel free to contribute by opening issues or sending pull requests.
