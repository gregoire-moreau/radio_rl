#!/usr/bin/env python3

import os
import zipfile
import argparse

parser = argparse.ArgumentParser(description='Zip or dezip a folder')
parser.add_argument('-z', '--zip', action='store_true')
parser.add_argument('-d', '--dezip', action='store_true')
parser.add_argument('folder_name')


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    args = parser.parse_args()
    if args.zip:
        zipf = zipfile.ZipFile(args.folder_name+'.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(args.folder_name, zipf)
        zipf.close()
    elif args.dezip:
        zipf = zipfile.ZipFile(args.folder_name+'.zip', 'r', zipfile.ZIP_DEFLATED, compresslevel=9)
        zipf.extractall(path=args.folder_name)
        zipf.close()
    else:
        raise Exception('Zip or dezip')
