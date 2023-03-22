from src.extract import *
from src.embed import *


class Programm:
    def __init__(self, parser_args):
        args = vars(parser_args)
        if args['key'] is not None:
            with open(args['key'], 'r') as file:
                self.mu = file.read().strip()
        if args['wm_file'] is not None:
            with open(args['wm_file'], 'r') as file:
                wm_hex = file.read().strip()
                wm = bin(int(wm_hex, 16))[2:].zfill(len(wm_hex) * 4)
                self.wm = wm + '0' * ((11 - len(wm) % 11) % 11)
        if args['image_file'] is not None:
            self.image_file = args['image_file']
        if args['images_list'] is not None:
            self.paths = args['images_list']
        if args['l'] is not None:
            self.l = args['l']

    def embed(self):
        img_arr = image_as_layers(self.image_file)
        img1, img2, img3, img4 = Embed(img_arr, self.mu, self.wm)
        Image.fromarray(img1).save('img1.png')
        Image.fromarray(img2).save('img2.png')
        Image.fromarray(img3).save('img3.png')
        Image.fromarray(img4).save('img4.png')
        print("Watermarked images in files img1.png, img2.png, img3.png, img4.png")

    def extract_watermark(self):
        img_arr = image_as_layers(self.image_file)
        wm = ExtractWatermark(img_arr, self.mu)[:self.l]
        wm = hex(int(wm, 2))[2:]
        print('Extracted watermark:', wm)

    def exctract_cover(self):
        path1, path2, path3, path4 = self.paths
        images = [image_as_layers(path1), image_as_layers(path2), image_as_layers(path3), image_as_layers(path4)]
        imgg = ExtractCoverImage(*images)
        Image.fromarray(imgg).save('new_image.png')
        print('Saved extracted image in file: new_image.png')
