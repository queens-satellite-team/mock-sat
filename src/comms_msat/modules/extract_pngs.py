# extract_pngs.py
# Extract PNGs from a file and put them in a pngs/ directory
import sys

with open("PythonAttempt/sent.png", "rb") as binary_file:
    binary_file.seek(0, 2)  # Seek the end
    num_bytes = binary_file.tell()  # Get the file size
    print(num_bytes)

    count = 0
    for i in range(num_bytes):
        binary_file.seek(i)
        eight_bytes = binary_file.read(8)
        print(eight_bytes)
        if eight_bytes == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":  # PNG signature
            count += 1
            print("Found PNG Signature #" + str(count) + " at " + str(i))

            # Next four bytes after signature is the IHDR with the length
            png_size_bytes = binary_file.read(4)
            png_size = int.from_bytes(png_size_bytes, byteorder="little", signed=False)

            # Go back to beginning of image file and extract full thing
            binary_file.seek(i)
            # Read the size of image plus the signature
            png_data = binary_file.read(png_size + 8)
            with open("PythonAttempt/img/pngs" + str(i) + ".png", "wb") as outfile:
                outfile.write(png_data)
