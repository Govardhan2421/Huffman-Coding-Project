import heapq
import os


class Huffman:
    # Constructor
    def __init__(self, path):
        self.path = path  # For storing the Actual path of the file
        self.heap = []  # Init an empty array for heap
        self.codes = {}
        self.reverse_mapping = {}

    """
    **************************************************************************************
    ********************************* Compression Module *********************************
    **************************************************************************************
    """

    def compressTheFile(self):
        # 1) Get name and extension of the file
        name_of_file, file_extension = os.path.splitext(self.path)

        # 2) Use in-built string method(split) to get the file name
        name_of_file = name_of_file.split("/")[1]

        # 3) Preserve the original path in old_path variable
        old_path = self.path

        # 4) Create a file with extension(.bin) inside Folder(compressedFiles)
        output_path = "compressedFiles/" + name_of_file + ".bin"

        # 5) If the fileType is Image, enter the below block
        if(file_extension in [".png", ".jpg"]):
            # Images cannot be simply compressed with Huffman, below method should be invoked for further processing
            self.handleImageFileCompression()
            # Store the original path to preserve the fileNames etc
            old_path = self.path
            # Change the path
            self.path = "filesToCompress/imageToText.txt"

        """
        **************************************************************************************
        ********************************* Actual Compression Begins *********************************
        **************************************************************************************
        """
        with open(self.path, 'r+') as file:
            # 1) Read contents of the file and strip any unwanted spaces
            content = file.read().strip()

            # 2) Build a Character Frequency Dictionary
            frequency = self.computeCharFrequency(content)

            # 3) Build a Heap with the frequency Values
            self.buildHeap(frequency)

            # 4) Merge the Nodes
            self.mergeNodes()
            # 5) Assgin Unique codes
            self.assignCodes()

            # 6) Now we have to encode the Text
            encoded_text = self.encodeText(content)
            padded_encoded_text = self.padEncodedText(encoded_text)

            b = self.getByteArray(padded_encoded_text)

            # 7) Dump the output in the below Files
            with open(output_path, 'wb') as output:
                output.write(bytes(b))

        # Now change the path to its original form
        self.path = old_path

        return output_path

    def handleImageFileCompression(self):
        """
        Objective: Images cannot be simply compressed with Huffman, below flow is necessary

        ImageFile(Byte Format) -> Convert To base64 -> Decode base64 to Text -> Apply Huffman compression
        """
        image_path = self.path

        with open(image_path, "rb") as image_file:
            import base64

            # 1) Convert Image to Base64
            text = base64.b64encode(image_file.read())

            # 2) Convert Base64 to text(String)
            text = text.decode("utf-8")

            # 3) Create a new file to store the text
            with open("filesToCompress/imageToText.txt", "w+") as file:
                file.write(text)

    def computeCharFrequency(self, text):
        # Init an emtpy Dictionary
        frequency = {}
        # Loop over every char in the Text
        for character in text:
            if character in frequency:
                frequency[character] += 1
            else:
                frequency[character] = 1

        return frequency

    def buildHeap(self, frequencyList):
        for key in frequencyList:
            node = self.HeapNode(key, frequencyList[key])
            heapq.heappush(self.heap, node)

    def mergeNodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.helper(root.left, current_code + "0")
        self.helper(root.right, current_code + "1")

    def assignCodes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.helper(root, current_code)

    def encodeText(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def padEncodedText(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def getByteArray(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    """
    **************************************************************************************
    ********************************* De-Compression Module ******************************
    **************************************************************************************
    """

    def decompress(self, compressed_file_path):

        # 1) Get name and extension of the file
        name_of_file, file_extension = os.path.splitext(self.path)
        name_of_file = name_of_file.split("/")[1]
        # 2) Set Path for storing the decompressed file
        output_path = "deCompressedFiles/"+name_of_file + "_decompressed" + file_extension

        with open(compressed_file_path, 'rb') as file:
            bitString = ""
            byte = file.read(1)

            while(len(byte) > 0):
                # ord() = Returns the number representing the unicode code of a specified character.
                byte = ord(byte)
                # bin() = Converts and returns the binary equivalent string of a given integer
                # rjust() = Will right align the string, using a specified character (space is default) as the fill character.
                bits = bin(byte)[2:].rjust(8, '0')
                bitString += bits
                byte = file.read(1)

            encoded_text = self.removePadding(bitString)

            decompressed_text = self.decodeText(encoded_text)

            if(file_extension in [".png", ".jpg"]):
                self.handleImageFileDeCompression(
                    decompressed_text, output_path)
            else:
                output_file = open(output_path, 'w')
                output_file.write(decompressed_text)
                output_file.close

        return output_path

    def removePadding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decodeText(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def handleImageFileDeCompression(self, decompressed_text, output_path):
        print("Something diff for",  output_path)

        text = decompressed_text
        text = text.encode("utf-8")
        with open(output_path, "wb") as file:
            import base64
            image = base64.b64decode(text)
            file = file.write(image)

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq
