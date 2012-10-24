__author__ = 'schinken'

import Image
import ImageFont
import ImageDraw

import ledutils
import ledloard

class DrawText:

    board_width  = 96
    board_height = 16

    banner_width = 0
    image_xy     = False

    def __init__(self, text, font_path):
        self.image_xy, self.banner_width = self.render_text(text, font_path)

    def get_image(self):
        return self.image_xy

    def get_frame_count(self):
        return self.banner_width-self.board_width+1

    def get_frame(self, num):
        
        frame = {}
        for x in xrange(self.board_width):
            frame[x] = self.image_xy[x+num]

        return frame

    def determine_font_size(self, text, font):

        for text_size in xrange(12, 42):

            fontobj = ImageFont.truetype(font, text_size)
            width, height = fontobj.getsize(text)

            if height > self.board_height:
                return ImageFont.truetype(font, text_size-1)

        return False

    def quantify_image(self, arr, banner_width):

        quantified = {}

        for x in xrange(banner_width):
            quantified[x] = {}
            for y in xrange(self.board_height):
                quantified[x][y] = int(ledutils.to_grayscale(arr[x,y]))

        return quantified

    def render_text(self, text, font_path):

        pad_front = 10

        # try to determine the best matching font size for boarsize
        font = self.determine_font_size(text, font_path)
        text_width, text_height = font.getsize(text)

        # calculate banner width for rotation
        banner_width = text_width+self.board_width+pad_front

        im = Image.new(mode='RGB', size=(banner_width, self.board_height), color=(0,0,0))
        
        # draw text on raw image
        draw = ImageDraw.Draw(im)
        draw.text( (self.board_width+pad_front,0), text, font=font )

        image_xy = im.load()
        return self.quantify_image( image_xy, banner_width ), banner_width

