proxpy
=======

`proxpy` is a simple script for generating sheets of Magic: The Gathering
proxy card images. It downloads the necessary images from Scryfall and
caches them locally, then generates sheets of card images to print.

Still tweaking it, stay tuned.

Install
-------

1. As root/administrator: `./setup.py install`


Usage
-----

```
usage: proxpy [-h] [-c CACHE_DIR] [-o OUTPUT_DIR] [-n] input

Simple utility for generating sheets of MtG proxies.

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -c CACHE_DIR, --cache-dir CACHE_DIR
                        Specify directory for storing and retreiving cached images.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Specify directory for output sheet files.
  -n, --no-cache        Do not use the cache directory; download all images.
```

Input files should be a list of cards, one per line, prefixed by a number
and a space. For example:

```
1 Skullclamp
2 Wrenn and Six
1 Bonecrusher Giant
```

Output
------

Card images are cached under the system's user appdata directory:

  - Linux: `~/.local/share/proxpy/card_images`
  - MacOS: `~/Library/Application Support/proxpy/card_images`
  - Windows: `C:\Users\<user>\AppData\Local\proxpy\proxpy\card_images`

Sheets are saved to the current working directory by default, but this can be overriden with the `-o` option (see above). All sheets are numbered.

Sheets look like this:

![Example Sheet](https://github.com/demern/proxpy/blob/master/examples/sheets/sheet1.png)
