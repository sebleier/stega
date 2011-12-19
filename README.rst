Stega
=====


Stega is a simple steganography tool that allows you to losslessly embed
messages into images.  The image that comes back is same as the original.

The only requirement is that you use a lossless image format, so no jpeg
images will work.


Usage::

    image = Image.new('RGB', (111, 111))
    msg = "What hath God wrought. "
    s = Stega(image)
    s.add_message(msg)

    im, message = s.split()
    assert message == msg

Run tests::

    $ python tests/__init__.py
