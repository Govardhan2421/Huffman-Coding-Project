# This is the Start of our Program

import time
from alive_progress import alive_bar
import sys
sys.dont_write_bytecode = True  # Prevents .pyc(ByteCode) files creation

if __name__ == "__main__":
    from HuffmanCoding import HuffmanCoding

    # 1) Path of the file to be compressed
    path = "filesToCompress/samplePic.jpg"

    # 2) Create an Object of Class(HuffmanCoding)
    huffman = HuffmanCoding(path)

    # 3) Compress method Returns the path of the compresses file
    output_path = ""
    with alive_bar(len(range(100))) as bar:
        print("Compressing.....")
        output_path = huffman.compress()
        for item in range(100):
            bar()
            time.sleep(0.01)
    print("Compressed")
    print("Compressed file path: " + output_path)

    # 4) deCompress method Returns the path of the deCompressesed file
    decom_path = ""
    with alive_bar(len(range(100))) as bar:
        print("DeCompressing.....")
        decom_path = huffman.decompress(output_path)
        for item in range(100):
            bar()
            time.sleep(0.01)
    print("Decompressed file path: " + decom_path)
