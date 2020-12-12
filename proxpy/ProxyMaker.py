from PIL import Image
import appdirs
import os
import requests
import shutil
import sys
import tempfile
import time

class ProxyMaker():
    def __init__(self, cache_dir, output_dir, no_cache=False):
        # Default directories for application data
        self.no_cache = no_cache
        self.output_dir = output_dir
        if self.no_cache:
            # '--no-cache' specified--store images in a temporary directory
            self.cache_dir = tempfile.TemporaryDirectory().name
            print(self.cache_dir)
        else:
            self.cache_dir = cache_dir

    def __del__(self):
        if self.no_cache:
            shutil.rmtree(self.cache_dir)

    # Given a cardname, download the image from Scryfall
    def download_card(self, cardname):
        linkname = cardname.replace(" ", "+").lower()
        outname = cardname.replace(" ", "_") + ".png"
        outfile = os.path.join(self.cache_dir, outname)

        if os.path.exists(outfile):
            print("Card image for {} already exists at {}.".format(cardname,outfile))
            return outfile

        # Per Scryfall's request, insert a 0.1 second delay between downloads
        time.sleep(0.1)

        # Request card image
        print("Downloading card image for {} to {}...".format(cardname, outfile))
        URI = "https://api.scryfall.com/cards/named?exact={}&format=image&version=png".format(linkname)
        r = requests.get(URI, stream=True)
        if r.status_code == 200:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir, exist_ok=True)
            with open(outfile, 'wb+') as f:
                # Write image file
                shutil.copyfileobj(r.raw, f)
                # Resize to appropriate dimensions
                print("Resizing card image for {}...".format(cardname))
                resized = Image.open(outfile).resize((791,1107), Image.ANTIALIAS)
                resized.save(outfile, dpi=(315,315))
            return outfile
        else:
            print("{} - Unable to download card image for {}".format(r.status_code, cardname))
            return 1

    # Create sheets (with maximum of 9 cards per sheet)
    # 'image_list' is a list of file paths which are images generated via 
    # the 'download_card' function.
    def create_sheets(self, image_list):
        space = 15
        card_w = 791
        card_h = 1107
        sheet_w = 2678
        sheet_h = 3465
        border_w = (sheet_w - card_w*3 + space*2)//2
        border_h = (sheet_h - card_h*3 + space*2)//2

        # Create output directory if needed
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        # Fit 9 images per sheet, generate the required
        # number of sheets to exhaust the input list.
        for i in range(0, len(image_list)//9 + 1):
            print("Generating sheet {}...".format(i+1))
            sheetname = "sheet{}.png".format(i+1)
            outfile = os.path.join(self.output_dir, sheetname)

            # Empty sheet to paste card images onto
            empty_sheet = Image.new('RGBA', (sheet_w, sheet_h), (255, 255, 255, 255))
            first = 9*i
            last = first + 9

            # Create + save the i'th sheet
            for j in range(first, last):
                # We hit the end, bye
                if j == len(image_list):
                    print("Sheet {} saved to {}.".format(i+1, outfile))
                    return 0

                # Paste card image into sheet at appropriate offset
                card_image = Image.open(image_list[j], 'r')
                offset_w = int(border_w + (j%3) * (card_w + space)) 
                offset_h = int(border_h + ((j - 9*i)//3) * (card_h + space))
                empty_sheet.paste(card_image, (offset_w, offset_h))
                empty_sheet.save(outfile, dpi=(315,315))
            print("Sheet {} saved to {}.".format(i+1, outfile))

    # Parse a file containing a list of cardnames and download images for
    # those not already present locally, then create sheets of 9 cards and
    # save those to the current directory.
    def process_input(self, input_file):
        if not os.path.exists(input_file):
            print("Error: Input file {} does not exist.".format(input_file))
            return 1

        input_list = []
        with open(input_file) as f:
            # Loop through lines of input list
            while True:
                line = f.readline()
                # EOF condition
                if not line:
                    break

                count, name = line.rstrip().split(" ", 1)
                # Download card image if needed
                image_file = self.download_card(name)  
                if image_file != 1:
                    # Might want multiple copies of a card
                    for i in range(0, int(count)):
                        input_list.append(image_file)
                else:
                    print("Error downloading {}, skipping it.".format(name))
                    continue
        self.create_sheets(input_list)
