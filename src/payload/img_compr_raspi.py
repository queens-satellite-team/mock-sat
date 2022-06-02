## Run on raspberry pi!

from picamera import PiCamera
from time import sleep
from datetime import datetime
from PIL import Image
from matplotlib import image
from matplotlib import pyplot as plt
import os

class PiCam(PiCamera):
    
    def __init__(self):
        super().__init__()
        print('called PiCam init!')

    def shot(self, filename:str='image.jpg'):
        self.start_preview()
        sleep(2)
        self.capture(filename)
        self.stop_preview()
        self.close()


def main():

    # set path names to be used in the main call
    image_path = "/home/pi/Desktop/image.jpg"
    compressed_image_path = "/home/pi/Desktop/image_compressed.jpg"
    
    # create a picam object and make it take a photo
    cam = PiCam()
    cam.shot(image_path)

    # Compress the image
    img = Image.open(image_path)
    width, height = img.size
    scale_factor = 10
    img_compressed = img.resize((int(width / scale_factor), int(height / scale_factor)))
    img_compressed.save(compressed_image_path)
    img_size = os.path.getsize(image_path)
    img_compressed_size = os.path.getsize(compressed_image_path)

    # Plot
    plt.figure(figsize=(15,12))

    plt.subplot(121)
    plt.imshow(img)
    #plt.title(f"Original Image ({(img_size / 1024):.2f} kB)")

    plt.subplot(122)
    plt.imshow(img_compressed)
    #plt.title(f"Compressed Image ({(img_compressed_size / 1024):.2f} kB)")

    plt.show()
    plt.savefig("/home/pi/Desktop/compression_results.png")

if __name__ == '__main__':
    main()