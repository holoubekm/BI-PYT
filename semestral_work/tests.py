#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tento testovací skript předpokládá, že výkonná část interpretru je uložena v adresáři „brainx“ (a tudíž volána pomocí „__main__.py“). Souhrnně je adresářová struktura semestrálky následující:

semestrálka.kostra/
    brainx/
        __main__.py
        ...
    tests/
        ...
    README.txt
    tests.py

Postupně se volají následující testy:

# memory tests
brainx "[-]" -m b'\x03\x02' -p 1 -t
brainx "[[-]<]" -m b'\x03\x03\x00\x02\x02' -p 4 -t
brainx "[<]" -m b'\x03\x03\x00\x02\x02' -p 4 -t
brainx "[>]" -m b'\x03\x03\x00\x02\x02' -t
brainx "[>+<-]" -m b'\x03\x03' -t
brainx "[>+>+<<-]>>[<<+>>-]" -m b'\x03\x03' -t
brainx "[>-<-]" -m b'\x03\x05' -t

# basic brainfuck tests
brainx tests/hello1.b
brainx tests/hello2.b
brainx -t tests/hello2.b
brainx tests/hello2t.b

# brainfuck with input
brainx tests/numwarp_input.b

# basic PNG
brainx tests/sachovnice.jpg
brainx tests/sachovnice_paleta.png

# brainloller
brainx tests/HelloWorld.png
brainx -t tests/HelloWorld.png

"""

import subprocess


#
# memory tests
#

# test 0a
print('\n\nTest 0a: brainx "[-]" -m b\'\\x03\\x02\' -p 1 -t')
print('\tvynulování aktuální, ale pouze aktuální, buňky')
args = ['python3', 'brainx', '"[-]"', '-m', r"b'\x03\x02'", '-p', '1', '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory01_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 0b
print('\n\nTest 0b: brainx "[[-]<]" -m b\'\\x03\\x03\\x00\\x02\\x02\' -p 4 -t')
print('\tvynulování všech nenulových buněk doleva')
args = ['python3', 'brainx', '"[[-]<]"', '-m', r"b'\x03\x03\x00\x02\x02'", '-p', '4', '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory02_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 0c
print('\n\nTest 0c: brainx "[<]" -m b\'\\x03\\x03\\x00\\x02\\x02\' -p 4 -t')
print('\tpřesun na první nenulovou buňku doleva')
args = ['python3', 'brainx', '"[<]"', '-m', r"b'\x03\x03\x00\x02\x02'", '-p', '4', '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory03_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 0d
print('\n\nTest 0d: brainx "[>]" -m b\'\\x03\\x03\\x00\\x02\\x02\' -t')
print('\tpřesun na první nenulovou buňku doprava')
args = ['python3', 'brainx', '"[>]"', '-m', r"b'\x03\x03\x00\x02\x02'", '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory04_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 0e
print('\n\nTest 0e: brainx "[>+<-]" -m b\'\\x03\\x03\' -t')
print('\tdestruktivní přičtení aktuální buňky k buňce následující')
args = ['python3', 'brainx', '"[>+<-]"', '-m', r"b'\x03\x03'", '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory05_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 0f
print('\n\nTest 0f: brainx "[>+>+<<-]>>[<<+>>-]" -m b\'\\x03\\x03\' -t')
print('\tnedestruktivní přičtení aktuální buňky k buňce následující')
args = ['python3', 'brainx', '"[>+>+<<-]>>[<<+>>-]"', '-m', r"b'\x03\x03'", '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory06_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 0g
print('\n\nTest 0g: brainx "[>-<-]" -m b\'\\x03\\x05\' -t')
print('\tdestruktivní odečtení aktuální buňky od buňky následující')
args = ['python3', 'brainx', '"[>-<-]"', '-m', r"b'\x03\x05'", '-t']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory07_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out


#
# basic brainfuck tests
#

# test 1
print('\n\nTest 1: brainx tests/hello1.b')
print('\tHelloWorld s \\n')
args = ['python3', 'brainx', 'tests/hello1.b']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b'Hello World!\n'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''

# test 2a
print('\n\nTest 2a: brainx tests/hello2.b')
print('\tHelloWorld bez \\n')
args = ['python3', 'brainx', 'tests/hello2.b']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''

# test 2b
print('\n\nTest 2b: brainx -t tests/hello2.b')
print('\tHelloWorld bez \\n plus log')
args = ['python3', 'brainx', '-t', 'tests/hello2.b']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/hello2_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# test 2c
print('\n\nTest 2c: brainx tests/hello2t.b')
print('\tHelloWorld bez \\n plus dva průběžné logy')
args = ['python3', 'brainx', 'tests/hello2t.b']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/hello2t_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
with open('tests/hello2t_debug_02.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_02.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out


#
# brainfuck with input
#

# test 3
print('\n\nTest 3: brainx tests/numwarp_input.b')
print('\tnumwarp.b pro vstup "123"')
args = ['python3', 'brainx', 'tests/numwarp_input.b']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b'    /\\\n     /\\\n  /\\  /\n   / \n \\ \\/\n  \\\n   \n'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''


#
# basic PNG
#

# test 4a
print('\n\nTest 4a: brainx tests/sachovnice.jpg')
print('\tumíme jen PNG')
args = ['python3', 'brainx', 'tests/sachovnice.jpg']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
assert p.returncode == 4
#print( "error:", error )
assert b'PNGWrongHeaderError' in error

# test 4b
print('\n\nTest 4b: brainx tests/sachovnice_paleta.png')
print('\tumíme jen některá PNG')
args = ['python3', 'brainx', 'tests/sachovnice_paleta.png']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
assert p.returncode == 8
#print( "error:", error )
assert b'PNGNotImplementedError' in error


#
# brainloller
#

# test 5a
print('\n\nTest 5a: brainx tests/HelloWorld.png')
print('\tnačtení dat z obrázku HelloWorld.png')
args = ['python3', 'brainx', 'tests/HelloWorld.png']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''

# test 5b
print('\n\nTest 5b: brainx -t tests/HelloWorld.png')
print('\tnačtení dat z obrázku HelloWorld.png plus log')
args = ['python3', 'brainx', '-t', 'tests/HelloWorld.png']
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
#assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/HelloWorld_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out


#
# everything went OK
#
print('\n\n', '-'*70, '\n', 'OK: All tests passed.')
