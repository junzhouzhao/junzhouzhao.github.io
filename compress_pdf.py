#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created on 2022-04-22 10:00 by J. Zhao

import os
import argparse

CMD = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile={} '{}'"


def pretty_size(x):
    if x < 1024: return str(x)
    if x < 2**20: return '{:d}K'.format(x // 2**10)
    if x < 2**30: return '{:d}M'.format(x // 2**20)
    return '{:d}G'.format(x // 2**30)

def list_large_files(pdf_dir, size, echo=True):
    SIZE_THRESHOLD = size * 1024 * 1024
    large_files = []
    for root, dirs, files in os.walk(pdf_dir):
        if root.find('Thesis') != -1 or root.find('Slides') != -1: continue
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext != '.pdf': continue
            full_path_file = os.path.join(root, filename)
            size_before = os.path.getsize(full_path_file)
            if size_before > SIZE_THRESHOLD:
                large_files.append((full_path_file, size_before))
    if echo:
        for f, s in sorted(large_files, key=lambda x: -x[1]):
            print(f, pretty_size(s))
    return large_files

def compress(large_files):
    for full_path_file, size_before in large_files:
        print(full_path_file, pretty_size(size_before), end = ' ', flush=True)
        try:
            rst = os.popen(CMD.format("tmp.pdf", full_path_file)).read()
            if not rst:
                size_after = os.path.getsize("tmp.pdf")
                print(pretty_size(size_after))
                if size_after < size_before - 512:
                    os.system("mv tmp.pdf '{}'".format(full_path_file))
                else:
                    print("no change to file because no size reduction")
            else:
                print("\nError: ", rst, "\nno change to file due to error")
        except: pass


parser = argparse.ArgumentParser(description='Compress large pdf files.')
parser.add_argument('--list', action='store_true', help="list large files")
parser.add_argument('--compress', action='store_true', help="compress large files")
parser.add_argument('--size', type=int, default=1, help="size threshold (Mb), default 1")
parser.add_argument('pdfdir', default=".", help="pdf directory")
args = parser.parse_args()

if args.list:
    list_large_files(args.pdfdir, args.size)

if args.compress:
    compress(list_large_files(args.pdfdir, args.size, False))
