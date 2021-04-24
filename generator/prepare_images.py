import argparse
from PIL import Image, ImageDraw
import glob
import os
import math

def main():
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--images', metavar='path', default="/Users/laure/Documents/quarup/rugs_data/MaxiCosi/*",
                        help='Path (possibly including wildcards) to images.')
    args = parser.parse_args()

    images_path = args.images if args.images.endswith('.jpg') else args.images + '.jpg'

    input_images = glob.glob(images_path)

    if len(input_images) == 0:
        print("ERROR: no files found in path: {}".format(images_path))

    images_dir = os.path.dirname(os.path.realpath(input_images[0]))
    num_written = 0
    for single_image_path in input_images:
        img = Image.open(single_image_path).convert("RGBA") 

        # Stripped file name, e.g. /path/to/file.jpg -> file
        image_base = os.path.splitext(os.path.basename(single_image_path))[0]

        # Pixel Value which would be used for
        # replacement 
        rep_value = (0, 0, 0, 0)

        # Flood fill four times starting from each corner of the image.
        #
        # Alternatively we could have expanded the canvas with a default
        # color and run flood fill once.
        #
        # Yeah, that would've been smarter.
        for x in [0, img.size[0] - 1]:
            for y in [0, img.size[1] - 1]:
                # Coordinates of the pixel whose value
                # would be used as seed
                seed = (x, y)
                ImageDraw.floodfill(img, seed, rep_value, thresh=10)

        # Downsample image. Large images don't load very well (if at all) on
        # mobile devices for Augmented Reality.
        max_size = 2048 * 2048
        orig_size = img.size[0] * img.size[1]
        if orig_size > max_size:
            height = math.sqrt(max_size * img.size[1] / img.size[0])
            width = height * img.size[0] / img.size[1]
            dest_size = (int(width), int(height))
            print("resizing {} from {} ({} pixels) to {} ({} pixels)".format(image_base, img.size, orig_size, dest_size, dest_size[0] * dest_size[1]))
            img = img.resize(dest_size)


        # Write out the image.
        output_path = os.path.join(images_dir, image_base + '.png')
        print('[{}] writing to {}'.format(num_written + 1, output_path))
        img.save(output_path)
        num_written += 1

    print("Wrote {} images to {}".format(num_written, images_dir))

if __name__ == "__main__":
    main()