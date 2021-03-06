# This is the Start of our Program

import time  # For Progress bar
from alive_progress import alive_bar  # For Progress bar
import sys
sys.dont_write_bytecode = True  # Prevents .pyc(ByteCode) files creation


def compressFile(hf):
    print("Compressing.....")
    with alive_bar(len(range(100))) as bar:
        output_path = hf.compressTheFile()
        for i in range(100):
            bar()
            time.sleep(0.01)
    print("File Compression Complete Succesfully")
    return output_path


def deCompressFile(hf, op):
    print("DeCompressing.....")
    with alive_bar(len(range(100))) as bar:
        decom_path = hf.decompress(op)
        for i in range(100):
            bar()
            time.sleep(0.01)
    return decom_path


if __name__ == "__main__":
    from Huffman import Huffman

    # 1) Path of the file to be compressed
    fileName="sampleText.txt"
    path = "filesToCompress/"+fileName

    # 2) Create an Object of Class(HuffmanCoding)
    huffman = Huffman(path)

    # 3) Method(Compress) returns the path of the compressed file
    compressed_file_path = compressFile(huffman)
    print("Compressed file Location: " + compressed_file_path)

    # 4) Method(deCompress) Returns the path of the deCompressesed file
    decompressed_file_path = deCompressFile(huffman, compressed_file_path)

    print("Decompressed file path: " + decompressed_file_path)
