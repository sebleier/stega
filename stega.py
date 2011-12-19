

class Block(object):

    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.bits = 8

    def __iter__(self):
        x, y = self.x, self.y
        yield self.img.getpixel((x - 1, y - 1))[0]
        yield self.img.getpixel((x, y - 1))[0]
        yield self.img.getpixel((x + 1, y - 1))[0]
        yield self.img.getpixel((x - 1, y))[0]
        yield self.img.getpixel((x + 1, y))[0]
        yield self.img.getpixel((x - 1, y + 1))[0]
        yield self.img.getpixel((x, y + 1))[0]
        yield self.img.getpixel((x + 1, y + 1))[0]

    def __len__(self):
        return self.bits

    def get_value(self):
        return self.img.getpixel((self.x, self.y))[0]

    def set_value(self, value):
        color = list(self.img.getpixel((self.x, self.y)))
        color[0] = value
        self.img.putpixel((self.x, self.y), tuple(color))

    value = property(get_value, set_value)

    @property
    def avg(self):
        average = sum(value for value in self) / len(self)
        #print "average", average
        return average

    @property
    def avg_diff(self):
        diff = self.value - self.avg
        #print "diff", diff
        return diff

    @property
    def delta(self):
        if self.avg_diff < 0:
            d = min(self) - self.avg
        else:
            d = max(self) - self.avg
        #print "delta", d
        return d

    @property
    def s(self):
        if self.avg + 2 * self.avg_diff < 0 or pow(2, self.bits) - 2 < self.avg + 2 * self.avg_diff:
            return abs(self.delta)
        else:
            return float("inf")


class BlockSpace(object):

    def __init__(self, img):
        self.img = img
        self.width = self.img.size[0]
        self.height = self.img.size[1]

    def __iter__(self):
        for x in range(1, self.width - 7, 2):
            for y in range(1, self.height - 7, 2):
                yield Block(self.img, x, y)


class BitMessage(object):
    """
    Object to allow an index to select the nth bit in a message
    """
    def __init__(self, msg=""):
        self.msg = map(ord, msg)

    def __getitem__(self, index):
        return self.msg[index / 8] >> (index % 8) & 1

    def __setitem__(self, index, value):
        try:
            self.msg[index / 8] = self.msg[index / 8] | (value << index % 8)
        except IndexError:
            self.msg.append(0)
            self.msg[index / 8] = self.msg[index / 8] | (value << index % 8)

    @property
    def message(self):
        return "".join(map(chr, self.msg))

    def __len__(self):
        return len(self.msg) * 8

    def __str__(self):
        return self.message


class Stega(object):

    def __init__(self, img):
        self.img = img.copy()
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.B = BlockSpace(self.img)

    @property
    def s(self):
        if getattr(self, '_s', None) is not None:
            return self._s

        S = []
        for block in self.B:
            S.append(block.s)
        self._s = min(S)

        return self._s

    def add_message(self, msg):
        n = 0
        W = BitMessage(msg)

        for b in self.B:
            if abs(b.delta) < self.s:
                b.value = b.avg + 2 * b.delta + W[n]
                n += 1
                if n == len(W):
                    break

    def save(self, name):
        self.img.save(name)

    def close(self):
        self.img.close()

    def split(self):
        W = BitMessage()
        n = 0
        for b in self.B:
            if b.value - b.avg < 0:
                delta = min(b) - b.avg
            else:
                delta = max(b) - b.avg
            if delta < self.s:
                bit = (b.value - b.avg) % 2
                W[n] = bit
            if abs(delta) < self.s:
                b.value = (b.value + b.avg - bit) / 2
                n += 1
        return self.img, "".join(filter(lambda c: ord(c) != 0, W.message))
