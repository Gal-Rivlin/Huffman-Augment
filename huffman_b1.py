from ordered_list import OrderedList
from huffman_bit_writer import *
import os.path


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # stored as an integer - the ASCII character code value
        self.freq = freq  # the freqency associated with the node
        self.left = None  # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return self.char == other.char

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        elif self.freq == other.freq:
            if self.char < other.char:
                return True
            return False
        return False


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    f = open(filename, 'r')
    content = f.read()
    char_list = [0] * 256
    for i in content:
        char_list[ord(i)] += 1
    f.close()
    return char_list


#test1 = cnt_freq("file2.txt")
#print(test1[96:104])


def come_before(node1, node2, root):
    if node1.freq < node2.freq:
        root.left = node1
        root.right = node2
    elif node1.freq == node2.freq:
        if node1.char < node2.char:
            root.left = node1
            root.right = node2
        else:
            root.left = node2
            root.right = node1
    else:
        root.left = node2
        root.right = node1
    return


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    if len(char_freq) == 0 or None:
        return None
    o_list = OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] > 0:
            o_list.add(HuffmanNode(i, char_freq[i]))
        else:
            continue

    while o_list.size() > 1:

        # temp = o_list.python_list()
        # for i in temp:
        #     print(str(i.char), end=", ")
        # print("before")

        total = 0
        node1 = o_list.pop(0)
        total += node1.freq
        node2 = o_list.pop(0)
        total += node2.freq
        root_char = -1
        if node1.freq > node2.freq:
            root_char = node1.char
        elif node1.freq == node2.freq:
            if node1.char < node2.char:
                root_char = node1.char
            else:
                root_char = node2.char
        else:
            root_char = node2.char
        root = HuffmanNode(root_char, total)
        come_before(node1, node2, root)
        o_list.add(root)

        # temp = o_list.python_list()
        # for i in temp:
        #     print(str(i.char), end=", ")
        # print("after")


    return o_list.pop(0)


#test2 = create_huff_tree(test1)


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    code_list = [''] * 256
    create_code_helper(node, '', code_list)
    return code_list


def create_code_helper(root, code, code_list):
    if root.left is None and root.right is None:
        code_list[root.char] = code
        return
    if root.left is not None:
        create_code_helper(root.left, code + '0', code_list)
    if root.right is not None:
        create_code_helper(root.right, code + '1', code_list)
    return


#print(create_code(test2))


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    ans = ""
    for i in range(len(freqs)):
        if freqs[i] > 0:
            ans += str(i) + " " + str(freqs[i]) + " "
        else:
            continue
    return ans[:-1]


#print(create_header(test1))


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    if not os.path.isfile(in_file):
        raise FileNotFoundError
    freq_list = cnt_freq(in_file)
    header = create_header(freq_list)
    # print(header)
    huff_tree = create_huff_tree(freq_list)
    code_list = create_code(huff_tree)
    #print(code_list)
    ans = ""

    f = open(in_file, 'r')
    content = f.read()
    for c in content:
        ans += code_list[ord(c)]
    f.close()
    # print(header)
    out = open(out_file, 'a')
    out.truncate(0)
    out.write(header + "\n")
    # print(ans)
    out.write(ans)
    out.close()

    compress = HuffmanBitWriter(out_file[:-4]+"_compressed.txt")
    compress.write_str(header+"\n")
    compress.write_code(ans)
    compress.close()

    return


huffman_encode('file1.txt' , 'file1-222.txt')