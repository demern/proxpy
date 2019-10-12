proxpy
=======

`proxpy` is a simple script for generating sheets of Magic: The Gathering
proxy card images. It downloads the necessary images from Scryfall and
caches them locally, then generates sheets of card images to print.

Still developing + tweaking, stay tuned.

Dependencies
------------

  - `python3-pil`
  - `python3-requests`
  - `python3-appdirs`

Usage
-----

`./proxpy <input file>`

Input files should be a list of cards, one per line, prefixed by a number
and a space. For example:

```
1 Skullclamp
2 Wrenn and Six
1 Bonecrusher Giant // Stomp
```

Output
------

Card images are cached under the system's user appdata directory:

  - Linux: `~/.local/share/proxpy/card_images`
  - MacOS: `~/Library/Application Support/proxpy/card_images`
  - Windows: `C:\Users\<user>\AppData\Local\proxpy\proxpy`

Sheets are saved to the current working directory and are numbered.

Sheets look like this:

![Example Sheet](https://github.com/demern/proxpy/blob/master/examples/sheets/sheet1.png)
