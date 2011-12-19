from setuptools import setup

setup(
    name = "stega",
    url = "http://github.com/sebleier/stega/",
    author = "Sean Bleier",
    author_email = "sebleier@gmail.com",
    version = "0.0.1",
    packages = ["stega"],
    description = "A steganography tool for lossless message hiding in images.",
    install_requires=['PIL'],
)
