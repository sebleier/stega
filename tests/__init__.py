import os
import sys
import unittest
path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, path)

from stega import BitMessage, Block, BlockSpace, Stega
import Image


class TestBitMessage(unittest.TestCase):
    def test_usage_64(self):
        msg = BitMessage(chr(64))
        self.assertEqual(msg[0], 0)
        self.assertEqual(msg[1], 0)
        self.assertEqual(msg[2], 0)
        self.assertEqual(msg[3], 0)
        self.assertEqual(msg[4], 0)
        self.assertEqual(msg[5], 0)
        self.assertEqual(msg[6], 1)
        self.assertEqual(msg[7], 0)

    def test_usage_63(self):
        msg = BitMessage(chr(63))
        self.assertEqual(msg[0], 1)
        self.assertEqual(msg[1], 1)
        self.assertEqual(msg[2], 1)
        self.assertEqual(msg[3], 1)
        self.assertEqual(msg[4], 1)
        self.assertEqual(msg[5], 1)
        self.assertEqual(msg[6], 0)
        self.assertEqual(msg[7], 0)

    def test_usage_two_chars(self):
        msg = BitMessage(chr(1) + chr(255))
        self.assertEqual(msg[0], 1)
        self.assertEqual(msg[1], 0)
        self.assertEqual(msg[2], 0)
        self.assertEqual(msg[3], 0)
        self.assertEqual(msg[4], 0)
        self.assertEqual(msg[5], 0)
        self.assertEqual(msg[6], 0)
        self.assertEqual(msg[7], 0)

        self.assertEqual(msg[8], 1)
        self.assertEqual(msg[9], 1)
        self.assertEqual(msg[10], 1)
        self.assertEqual(msg[11], 1)
        self.assertEqual(msg[12], 1)
        self.assertEqual(msg[13], 1)
        self.assertEqual(msg[14], 1)
        self.assertEqual(msg[15], 1)

    def test_inputing_message(self):
        msg = BitMessage()
        msg[0] = 0
        msg[1] = 0
        msg[2] = 0
        msg[3] = 0
        msg[4] = 0
        msg[5] = 0
        msg[6] = 1
        msg[7] = 0

        self.assertEqual(msg.message, chr(64))

    def test_reassembling(self):
        msg = BitMessage("sean")
        self.assertEqual(str(msg), "sean")


def paint_color(image, width, height, color):
    for x in range(width):
        for y in range(height):
            image.putpixel((x, y), color)


class BlockTest(unittest.TestCase):
    def setUp(self):
        self.image = Image.new('RGB', (9, 9))
        paint_color(self.image, 9, 9, (200, 0, 0))

    def test_block(self):
        block = Block(self.image, 1, 1)
        iterations = 0
        for color in block:
            self.assertEqual(color, 200)
            iterations += 1
        self.assertEqual(iterations, 8)


class BlockSpaceTest(unittest.TestCase):
    def setUp(self):
        self.image = Image.new('RGB', (11, 11))
        paint_color(self.image, 11, 11, (200, 0, 0))

    def test_blockspace(self):
        blockspace = BlockSpace(self.image)
        bs_iterations = 0
        for block in blockspace:
            iterations = 0
            for color in block:
                self.assertEqual(color, 200)
                iterations += 1
            self.assertEqual(iterations, 8)
            bs_iterations += 1
        self.assertEqual(bs_iterations, 4)


class StegaTest(unittest.TestCase):
    def setUp(self):
        self.image = Image.new('RGB', (111, 111))
        self.original = self.image.copy()

    """
    Borked for me right now because of a PIL-inside-a-virtualenv problem.

    def test_stega(self):
        "
        Test steganography by saving image to disk, then reopening to
        extract message
        "

        s = Stega(self.image)
        s.add_message("sean")
        s.save("test_image.png")
        s.close()

        saved_image = Image.open('test_image.png')
        s = Stega(saved_image)
        im, message = s.split()
        self.assertEqual(message, "sean")
        self.assertEqual(im.tostring(), self.original.tostring())

    """
    def test_stega(self):
        """
        Test stega with in memory image representation, i.e. not saving
        to disk and reopening later.
        """
        msg = "What hath God wrought. "
        s = Stega(self.image)
        s.add_message(msg)
        im, message = s.split()
        self.assertEqual(message, msg)
        self.assertEqual(im.tostring(), self.original.tostring())


if __name__ == '__main__':
    unittest.main()
