import sys


class Brain:
    buffer = [0]
    data = []
    output = []
    png = []
    loop_cache = {}
    index = 0
    has_data = False
    pbm = False
    log_cnt = 1

    def __init__(self, code):
        self.code = code

        if code.find('!') >= 0:
            self.has_data = True
            self.data = code[code.find('!') + 1:]

    def right(self):
        self.index += 1
        if self.index >= len(self.buffer):
            self.buffer.append(0)

    def left(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0

    def inc(self):
        self.buffer[self.index] += 1
        if self.buffer[self.index] > 255:
            self.buffer[self.index] = 0

    def dec(self):
        self.buffer[self.index] -= 1
        if self.buffer[self.index] < 0:
            self.buffer[self.index] = 255

    def put(self):
        char = chr(self.buffer[self.index])
        self.output.append(self.buffer[self.index])
        print(char, end='', flush=True)

    def get(self):
        if self.has_data:
            if not len(self.data):
                return

            self.buffer[self.index] = ord(self.data[0]) % 256
            self.data = self.data[1:]
        else:
            val = ord(sys.stdin.read(1))
            self.buffer[self.index] = val

    def getValue(self):
        return self.buffer[self.index]

    def findRight(self, cur):
        if cur in self.loop_cache:
            return self.loop_cache[cur]

        ind = cur + 1
        depth = 1
        cnt = len(self.code)
        while ind < cnt:
            char = self.code[ind]
            if char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
            if depth == 0:
                self.loop_cache[cur] = ind
                return ind
            ind += 1
        raise Exception('No corresponding right bracket')

    def findLeft(self, cur):

        if cur in self.loop_cache:
            return self.loop_cache[cur]
        ind = cur - 1
        depth = -1
        while ind >= 0:
            char = self.code[ind]
            if char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
            if depth == 0:
                self.loop_cache[cur] = ind
                return ind
            ind -= 1
        raise Exception('No corresponding left bracket')

    def setMemory(self, memory):
        if memory:
            memory = memory[0][2:-1].replace('\\x', '')
            memory = bytearray.fromhex(memory)
            self.buffer = [x for x in memory]
            # print(self.buffer)

    def setPBM(self, pbm):
        self.pbm = pbm

    def setPtr(self, ptr):
        if ptr:
            self.index = int(ptr[0])

    def setPNG(self, png):
        self.png = png

    def writeLog(self, pnm=False, inp=True):
        chars = ['>', '<', '+', '-', '.', ',', '[', ']', '#']
        code = ''.join([x for x in self.code if x in chars])

        with open("debug_%02d.log" % (self.log_cnt), 'w') as log:
            log.write('# program data\n')
            log.write(code + '\n\n')
            log.write('# memory\n')
            log.write(str(bytes(self.buffer)))
            log.write('\n\n')
            log.write('# memory pointer\n')
            log.write(str(self.index))
            log.write('\n\n')

            if inp:
                log.write('# output\n')
            else:
                log.write('# input\n')
            log.write(str(bytes(self.output)))
            log.write('\n\n')
            if self.png:
                log.write('# RGB input\n[\n')
                for row in self.png:
                    log.write('    ' + str(row) + ',\n')
                log.write(']\n\n')
            if pnm:
                if inp:
                    log.write('# output\n')
                else:
                    log.write('# input\n')

                width = len(self.png[0])
                height = len(self.png)
                log.write('P6\n' + str(width) + ' ')
                log.write(str(height) + ' ')
                written = 0
                for row in self.png:
                    for pix in row:
                        if written % width == 0:
                            log.write('\n')
                        log.write(str(pix[0]) + ' ')
                        log.write(str(pix[1]) + ' ')
                        log.write(str(pix[2]) + ' ')
                        written += 1
                log.write('\n\n')
        self.log_cnt += 1

    def start(self):
        cnt = len(self.code)
        cur = 0
        while cur < cnt and cur >= 0:
            char = self.code[cur]

            if char == '>':
                self.right()
            elif char == '<':
                self.left()
            elif char == '+':
                self.inc()
            elif char == '-':
                self.dec()
            elif char == '.':
                self.put()
            elif char == ',':
                self.get()
            elif char == '[':
                if self.getValue() == 0:
                    cur = self.findRight(cur) + 1
                    continue
            elif char == ']':
                if self.getValue() != 0:
                    cur = self.findLeft(cur) + 1
                    continue
            elif char == '#':
                self.writeLog()
            cur += 1
