## Run on raspberry pi!

from picamera import PiCamera
from time import sleep
from PIL import Image
from matplotlib import image
from matplotlib import pyplot as plt
import os

camera = PiCamera()
image_path = "/home/pi/Desktop/image.jpg"
compressed_image_path = "/home/pi/Desktop/image_compressed.jpg"

# Take the picture
camera.start_preview()
sleep(5)  # camera warm-up time
camera.capture(image_path)
camera.stop_preview()
camera.close()

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
plt.title(f"Original Image ({(img_size / 1024):.2f} kB)")

plt.subplot(122)
plt.imshow(img_compressed)
plt.title(f"Compressed Image ({(img_compressed_size / 1024):.2f} kB)")

plt.show()
plt.savefig("/home/pi/Desktop/compression_results.png")
