Stega
=====


Stega is a simple `steganography`_ tool that allows you to losslessly embed
messages into images.  The image that comes back is same as the original.

The only requirement is that you use a lossless image format, so no jpeg
images will work.

This implementation was adapted from a `paper`_ titled "Lossless Data Hiding
in the Spatial Domain for High Quality Images", written by Hong Lin Jin,
Masaaki Fujiyoshi, and Hitoshi Kiya

.. _paper: http://203.64.187.41/htdocs-41/em/771.pdf
.. _steganography: http://en.wikipedia.org/wiki/Steganography

Usage::

    image = Image.new('RGB', (111, 111))
    msg = "What hath God wrought. "
    s = Stega(image)
    s.add_message(msg)

    im, message = s.extract()
    assert message == msg

Run tests::

    $ ./runtests

