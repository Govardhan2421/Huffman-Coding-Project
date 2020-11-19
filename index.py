# This is the Start of our Program

import sys
sys.dont_write_bytecode = True  # Prevents .pyc(ByteCode) files creation


if __name__ == "__main__":
    from HuffmanCoding import HuffmanCoding
    # 1) Path of the file to be compressed
    path = "filesToCompress/sampleText.txt"
    # 2) Create an Object of Class(HuffmanCoding)
    huffman = HuffmanCoding(path)
    # 3) Compress method Returns the path of the compresses file
    output_path = huffman.compress()
    print("Compressed file path: " + output_path)

    decom_path = huffman.decompress(output_path)
    print("Decompressed file path: " + decom_path)
