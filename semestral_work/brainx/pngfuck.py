import os
import zlib
import gzip
import base64
import binascii
import math
import sys


class PNGWrongHeaderError(Exception):

    def __init__(self, message):
        super(PNGWrongHeaderError, self).__init__(message)
        self.message = message


class ImgConverter:
    pix_data = []
    brain_data = ''
    png = None
    width = 0
    height = 0

    def __init__(self):
        pass

    def loadPNG(self, path):
        try:
            self.cur = 0
            self.img_size = os.path.getsize(path)
            with open(path, "rb") as f:
                self.img_data = f.read(self.img_size)
            self.inflate()
        except Exception as ex:
            print(ex)

    def loadCopter(self):
        ptr = (0, 0)
        way = 0
        data = ''
        while True:
            if ptr[0] >= self.height \
                or ptr[0] < 0 \
                or ptr[1] >= self.width \
                or ptr[1] < 0:
                break

            pos = (ptr[0] * self.width + ptr[1]) * 3
            r = self.pix_data[pos + 0]
            g = self.pix_data[pos + 1]
            b = self.pix_data[pos + 2]
            cmd = (65536 * r + 256 * g + b) % 11

            if cmd == 0:
                data += '>'
            elif cmd == 1:
                data += '<'
            elif cmd == 2:
                data += '+'
            elif cmd == 3:
                data += '-'
            elif cmd == 4:
                data += '.'
            elif cmd == 5:
                data += ','
            elif cmd == 6:
                data += '['
            elif cmd == 7:
                data += ']'
            elif cmd == 8:
                way += 1
                way %= 4
            elif cmd == 9:
                way -= 1
                way %= 4
            if way == 0:
                ptr = ptr[0], ptr[1] + 1
            elif way == 1:
                ptr = ptr[0] + 1, ptr[1]
            elif way == 2:
                ptr = ptr[0], ptr[1] - 1
            else:
                ptr = ptr[0] - 1, ptr[1]
        self.brain_data = data

    def loadLoller(self):
        pix_data = self.pix_data
        cmds = self.width * self.height
        ptr = (0, 0)
        way = 0
        data = ''
        while True:
            if ptr[0] >= self.height \
            or ptr[0] < 0 \
            or ptr[1] >= self.width \
            or ptr[1] < 0:
                break

            pos = (ptr[0] * self.width + ptr[1]) * 3
            pix = (pix_data[pos], pix_data[pos + 1], pix_data[pos + 2])

            if pix == (255, 0, 0):
                data += '>'
            elif pix == (128, 0, 0):
                data += '<'
            elif pix == (0, 255, 0):
                data += '+'
            elif pix == (0, 128, 0):
                data += '-'
            elif pix == (0, 0, 255):
                data += '.'
            elif pix == (0, 0, 128):
                data += ','
            elif pix == (255, 255, 0):
                data += '['
            elif pix == (128, 128, 0):
                data += ']'
            elif pix == (0, 255, 255):
                way += 1
                way %= 4
            elif pix == (0, 128, 128):
                way -= 1
                way %= 4
            else:
                cmds -= 1

            if way == 0:
                ptr = ptr[0], ptr[1] + 1
            elif way == 1:
                ptr = ptr[0] + 1, ptr[1]
            elif way == 2:
                ptr = ptr[0], ptr[1] - 1
            else:
                ptr = ptr[0] - 1, ptr[1]
        self.brain_data = data
        return cmds

    def toBrainFuck(self):
        row = []
        self.png = []
        pix_data = self.pix_data

        pos = 0
        while pos < len(pix_data):
            pix = (pix_data[pos], pix_data[pos + 1], pix_data[pos + 2])
            row.append(pix)
            if len(row) >= self.width:
                self.png.append(row)
                row = []
            pos += 3

        self.loadLoller()
        if len(self.brain_data) < 10:
            self.loadCopter()

        return self.brain_data

    def getPNG(self):
        return self.png

    def bytesToNum(self, start, end):
        val = 0
        for x in range(start, start + end):
            val = val * 256 + self.img_data[x]
        return val

    def numToBytes(self, size):
        data = []
        for x in [3, 2, 1, 0]:
            data.append(size // (256 ** x))
            size %= (256 ** x)
        return bytes(data)

    def getBpp(self):
        if self.img_type == 2:
            return self.bpp * 3
        elif self.img_type >= 4:
            return (self.img_type - 2) * self.bpp
        return self.bpp

    def paethPredictor(self, a, b, c):
        p = a + b - c
        pa = (p - a) if p > a else (a - p)
        pb = (p - b) if p > b else (b - p)
        pc = (p - c) if p > c else (c - p)
        return a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)

    def unfilterLine(self, line, prev, ftype):
        bpp = self.getBpp()
        bw = int((bpp + 7) // 8)
        length = int((self.width * bpp + 7) // 8)
        pred = self.paethPredictor

        if ftype == 0:
            pass
        elif ftype == 1:
            for x in range(bw, length):
                line[x] = (line[x] + line[x - bw]) % 256
        elif ftype == 2 and prev:
            for x in range(0, length):
                line[x] = (line[x] + prev[x]) % 256
        elif ftype == 3:
            if prev:
                for x in range(0, bw):
                    line[x] = (line[x] + prev[x] // 2) % 256
                for x in range(bw, length):
                    line[x] = (line[x] + ((line[x - bw] + prev[x]) // 2)) % 256
            else:
                for x in range(bw, length):
                    line[x] = (line[x] + line[x - bw] // 2) % 256
        elif ftype == 4:
            if prev:
                for x in range(0, bw):
                    line[x] = (line[x] + pred(0, prev[x], 0)) % 256
                for x in range(bw, length):
                    val = pred(line[x - bw], prev[x], prev[x - bw])
                    line[x] = (line[x] + val) % 256
            else:
                for x in range(bw, length):
                    line[x] = (line[x] + pred(line[x - bw], 0, 0)) % 256
        else:
            raise Exception('Usage of unimplemented filter')

        return [x % 256 for x in line]

    def decode(self, data):
        bpp = self.getBpp()
        strt = 0
        leng = int((self.width * bpp + 7) // 8)
        unfilt = self.unfilterLine

        prev = []
        out = []
        for y in range(0, self.height):
            ftype = data[strt]
            prev = unfilt(data[strt + 1: strt + leng + 1], prev, ftype)
            out += prev
            strt += 1 + leng
        self.pix_data = out

    def inflate(self):
        size = self.bytesToNum(8, 4)
        if size < 13:
            raise Exception('Expecting at lest 13 bytes header')
        ref = b'\x49\x48\x44\x52'

        if ref != self.img_data[12:16]:
            raise Exception('Expecting IHDR')
        self.width = self.bytesToNum(16, 4)
        self.height = self.bytesToNum(20, 4)
        self.bpp = self.img_data[24]
        self.img_type = self.img_data[25]
        self.deflate = self.img_data[26]
        self.filter = self.img_data[27]
        self.interlaced = self.img_data[28]

        if self.interlaced != 0:
            raise Exception('Interlaced pngs not supported')

        if self.bpp != 8:
            raise Exception('The only one supported depth is 8 bpp')

        if self.img_type != 2:
            sys.stderr.write('PNGNotImplementedError\n')
            sys.exit(8)

        pos = 8 + 4 + 4 + size + 4

        header_data = b'\x49\x44\x41\x54'
        header_end = b'\x49\x45\x4e\x44'
        data = b''
        while True:
            size = self.bytesToNum(pos, 4)
            pos += 4
            header = self.img_data[pos:pos + 4]
            pos += 4
            if size == 0 and header == header_end:
                break
            elif header == header_data:
                data += self.img_data[pos:size + pos]
                if self.img_type != 2:
                    raise Exception('Unsupported png type.')
            crc2 = binascii.crc32(self.img_data[pos - 4: size + pos])
            pos += size
            crc1 = self.bytesToNum(pos, 4)
            if crc1 != crc2:
                raise Exception('Damaged image file, crc doesn\'t match')
            pos += 4

        ret = []
        ret += zlib.decompress(data)
        self.decode(ret)

    def rev(self, data):
        out = []
        dataLen = len(data) // 3
        for x in range(0, dataLen):
            out.extend(data[3 * (dataLen - x - 1): 3 * (dataLen - x)])
        return out

    def savePNG(self, path, pixdata):
        if not pixdata:
            raise Exception('Nothing to save')

        width = self.width
        height = self.height
        try:
            with open(path, 'wb') as f:
                #write png header
                f.write(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d')
                header = b'\x49\x48\x44\x52'
                header += self.numToBytes(width)
                header += self.numToBytes(height)
                header += b'\x08\x02\x00\x00\x00'
                header += self.numToBytes(binascii.crc32(header))
                #write IHDR
                f.write(header)

                #rite IDAT
                compr = zlib.compress(pixdata)
                f.write(self.numToBytes(len(compr)))
                header = b'\x49\x44\x41\x54'
                header += compr
                header += self.numToBytes(binascii.crc32(header))
                f.write(header)
                #write IEND
                f.write(b'\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82')

        except Exception as a:
            print(a)
            print('Exception while writing image')

    def saveLoller(self, path):
        width = 64
        left = b'\x00\x80\x80'
        right = b'\x00\xff\xff'

        out = b''
        data = self.pix_data
        dataLen = len(data)
        lineLen = width * 3
        written = 0
        line = 0
        even = True

        while written < dataLen:
            out += b'\x00'
            if line != 0:
                out += left
            else:
                out += b'\x00\x00\x00'

            if dataLen - written > lineLen:
                if even:
                    out += bytes(data[line * lineLen: (line + 1) * lineLen])
                else:
                    out += bytes(self.rev(data[line * lineLen: (line + 1) * lineLen]))
            else:
                if even:
                    out += bytes(data[line * lineLen:])
                else:
                    out += bytes(self.rev(data[line * lineLen:]))
                out += bytes(lineLen - (dataLen - written))
            out += right
            line += 1
            written += lineLen
            even = not even

        width += 2

        # print(out)
        self.width = width
        self.height = line
        self.savePNG(path, out)

    def saveCopter(self, path):
        self.savePNG(path, bytes(self.pix_data))

    def getBrain(self):
        return self.brain_data

    def brainToLoller(self, code):
        if self.pix_data:
            raise Exception('Image data already loaded')

        pixels = []
        for char in code:
            if char == '>':
                pixels += [255, 0, 0]
            elif char == '<':
                pixels += [128, 0, 0]
            elif char == '+':
                pixels += [0, 255, 0]
            elif char == '-':
                pixels += [0, 128, 0]
            elif char == '.':
                pixels += [0, 0, 255]
            elif char == ',':
                pixels += [0, 0, 128]
            elif char == '[':
                pixels += [255, 255, 0]
            elif char == ']':
                pixels += [128, 128, 0]

        self.bpp = 8
        self.img_type = 2
        self.deflate = 0
        self.filter = 0
        self.interlaced = 0

        self.brain_data = code
        self.pix_data = pixels

    def brainToCopter(self, code, png):
        output = []
        for x in range(0, len(png) // 3):
            if x % self.width == 0:
                output.append(0)
            r = png[x * 3 + 0]
            g = png[x * 3 + 1]
            b = png[x * 3 + 2]

            if x < len(code):
                cur = code[x]
                val = 10
                if cur == '>':
                    val = 0
                elif cur == '<':
                    val = 1
                elif cur == '+':
                    val = 2
                elif cur == '-':
                    val = 3
                elif cur == '.':
                    val = 4
                elif cur == ',':
                    val = 5
                elif cur == '[':
                    val = 6
                elif cur == ']':
                    val = 7
                loop = 0
                while (65536 * r + 256 * g + b) % 11 != val:
                    if loop % 3 == 0:
                        r += 1
                        r %= 256
                    elif loop % 3 == 1:
                        g += 1
                        g %= 256
                    else:
                        b += 1
                        b %= 256
            output += [r, g, b]

        self.bpp = 8
        self.img_type = 2
        self.deflate = 0
        self.filter = 0
        self.interlaced = 0

        self.brain_data = code
        self.pix_data = output
