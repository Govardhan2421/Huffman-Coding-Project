# This is the Start of our Program

import time  # For Progress bar
from alive_progress import alive_bar  # For Progress bar
import sys
sys.dont_write_bytecode = True  # Prevents .pyc(ByteCode) files creation


def compressFile(hf):
    print("Compressing.....")
    with alive_bar(len(range(100))) as bar:
        output_path = hf.compress()
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
    from HuffmanCoding import HuffmanCoding

    # 1) Path of the file to be compressed
    path = "filesToCompress/sampleText.txt"

    # 2) Create an Object of Class(HuffmanCoding)
    huffman = HuffmanCoding(path)

    # 3) Method(Compress) returns the path of the compressed file
    compressed_file_path = compressFile(huffman)
    print("Compressed file Location: " + compressed_file_path)

    # 4) Method(deCompress) Returns the path of the deCompressesed file
    decompressed_file_path = deCompressFile(huffman, compressed_file_path)

    print("Decompressed file path: " + decompressed_file_path)
