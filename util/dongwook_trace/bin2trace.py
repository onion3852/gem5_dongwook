### Read Me ###
# 1. Change binary file's name to "input.bin"
# 2. Change the root of "input.bin" to: /home/gem5/util/bin_trace/input.bin
# 3. Run this python file
# 4. "hex.txt" is the conversion of ".bin",
#    "information.txt" is the decoded one

from func import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--size",
    type=int,
    default=64,
    help="trace packet size(bytes), default is 64",
)
args = parser.parse_args()

# .bin -> .txt
input_file_path = "/home/gem5/util/dongwook_trace/input.bin"
output_file_path = "/home/gem5/util/dongwook_trace/hex.txt"
binary_to_text(input_file_path, output_file_path)

# Decode
input_file_path = "/home/gem5/util/dongwook_trace/hex.txt"
output_file_path = "/home/gem5/util/dongwook_trace/trace_converted.txt"
extract(input_file_path, output_file_path, args.size)
