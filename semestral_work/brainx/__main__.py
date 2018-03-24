#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os.path
import argparse
from brain import Brain
from pngfuck import ImgConverter


def debug(msg):
    print('Debug:\t', msg)


def error(msg):
    print('Error:\t', msg)

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('strings', metavar='N', type=str, nargs='?', help='separate source codes on the command line')
    parser.add_argument('--lc2f', action='store_true', help='extracts code from PNG file and saves it. Expects two arguments!')
    parser.add_argument('--f2lc', action='store_true', help='load brainfuck code and stores it inside a PNG image')
    parser.add_argument('-i', nargs="+")
    parser.add_argument('-o', nargs=1)
    parser.add_argument('-t', '--test', action='store_true', help='enables the verbose mode when the current state and memory is dumped to the log file')
    parser.add_argument('-m', '--memory', nargs=1, help="memory can be directly set using this switch")
    parser.add_argument('-p', '--memory-pointer', nargs=1, help='memory pointer can be directly set using this switch')
    parser.add_argument('--pnm', action='store_true', help='will dump code as an image in the PNM format')
    parser.add_argument('--pbm', action='store_true', help='will dump code as an image in the PBM format')
    args = parser.parse_args()


conv = ImgConverter()
codes = []
start = False

if args.lc2f:
    if len(args.i) <= 0 or len(args.o) <= 0:
        print('The --f2lc command requires -i and -o flags')

    conv.loadPNG(args.i[0])
    conv.toBrainFuck()

    out = args.o[1]
    data = conv.toBrainFuck()
    if out.startswith('>'):
        print(data)
        out = out[1:]
    with open(out, 'w') as output:
        output.write(data)
elif args.f2lc:
    if len(args.i) <= 0 or len(args.o) <= 0:
        print('The --f2lc command requires -i and -o flags')

    code = []
    with open(args.i[0]) as incode:
        code = ''
        for line in incode:
            code += line.strip()
    if len(args.i) == 1:
        conv.brainToLoller(code)
        conv.saveLoller(args.o[0])
    elif len(args.i) == 2:
        png = ImgConverter()
        png.loadPNG(args.i[1])
        conv.width = png.width
        conv.height = png.height
        conv.brainToCopter(code, png.pix_data)
        conv.saveCopter(args.o[0])
elif args.strings:
    start = True
    ifile = args.strings
    if os.path.isfile(ifile):
        if ifile.endswith('.b'):
            with open(ifile) as incode:
                code = ''
                for line in incode:
                    code += line.strip()
                codes.append([code, None])
        elif ifile.endswith('.png'):
            conv.loadPNG(ifile)
            codes.append([conv.toBrainFuck(), conv.getPNG()])
        else:
            sys.stderr.write('PNGWrongHeaderError\n')
            sys.exit(4)
    else:
        codes.append([ifile, None])
else:
    print('Please write down brainfuck program. Confirm with enter.:')
    codes.append([input().strip(), None])

for code, png in codes:
    brain = Brain(code)
    brain.setMemory(args.memory)
    brain.setPtr(args.memory_pointer)
    brain.setPNG(png)

    if start:
        brain.start()
    if args.test:
        brain.writeLog(args.pnm or args.pbm)

sys.exit(0)
