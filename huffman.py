from ordered_list import *
from huffman_bit_writer import *
from huffman_b2 import *
import os.path

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return type(other) is HuffmanNode \
                and self.freq == other.freq \
                and self.char == other.char
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        if self.freq > other.freq:
            return False
        if self.char < other.char:
            return True
        return False


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    freqlist = [0] * 256
    myfile = open(filename , 'r')
    line = myfile.readline()
    for char in line:
        num = int(ord(char))
        freqlist[num] += 1

    myfile.close()
    return freqlist


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    hufflist = OrderedList()
    for j in range(len(char_freq)):
        if char_freq[j] != 0:
            newnode = HuffmanNode(j , char_freq[j])
            hufflist.add(newnode)
    while hufflist.sentinel != hufflist.sentinel.next:
    #while hufflist.size() > 1:
        huf1 = hufflist.pop(0)
        huf2 = hufflist.pop(0)
        char = huf1.char
        if huf1.char > huf2.char:
            char = huf2.char
        frequency = huf1.freq + huf2.freq
        newhuf = HuffmanNode(char , frequency)
        newhuf.left = huf1
        newhuf.right = huf2
        hufflist.add(newhuf)

    return hufflist.sentinel.item



def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    hufflist = [''] * 256
    codelist = create_code_helper(node)
    impovelist = []
    for code in codelist:
        split = code.split(' ')
        for char in split:
            impovelist.append(char)
    for j in range(0,len(impovelist) - 1,2):
        char = int(impovelist[j + 1])
        hufflist[char] = impovelist[j]
    return hufflist


def create_code_helper(node):
    huffcodes = []
    if node.right == None and node.left == None:
        return [' {}'.format(str(node.char))]
    if node.right is not None:
        for num in create_code_helper(node.right):
            huffcodes.append('1' + num)
    if node.left is not None:
        for num in create_code_helper(node.left):
            huffcodes.append('0' + num)
    return huffcodes


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    headerstring = ''
    for j in range(len(freqs)):
        if freqs[j] != 0:
            headerstring += str(j) + ' ' + str(freqs[j]) + ' '

    stripped = headerstring.strip(' ')
    return stripped


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    hufflist = create_code(create_huff_tree(cnt_freq(in_file)))
    myfile = open(in_file, 'r')
    line = myfile.readline()
    bit_str = ''
    print(hufflist)
    for char in line:
        num = ord(char)
        bit_str += str(hufflist[num])

    o_f = open(out_file, 'w')
    newfile = HuffmanBitWriter(out_file[:-4] + "_compressed.txt")

    header_str = create_header(cnt_freq(in_file))
    o_f.write(header_str + '\n')
    newfile.write_str(header_str + '\n')
    newfile.write_code(bit_str)
    o_f.write(bit_str)

    newfile.close()
    o_f.close()


#bruh = cnt_freq('file1-2.txt')
#hmm = create_huff_tree(bruh)
#print(hmm.right.right.char)
#print(create_code(hmm))
#print(create_header(bruh))

huffman_encode('declaration.txt' , 'hello12.txt')