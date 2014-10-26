#!/usr/bin/env python3

"""
mb.py is a script to "mojibake"-ify binary data so that it can be copy/pasted
across (unicode-safe) terminals. It's designed to take up less space on screen than
base64. 
"""

import unittest
import argparse
import sys


def main(args):
	options = get_options(args)

	if options.files and options.mode == "encode":
		print(options.files)
		# TODO

	if options.mode == "encode":
		encode_stdin()
		return

	if options.mode == "decode":
		decode_stdin()
		return

	if options.mode == "interactive":
		interactive()
		return

	if options.mode == "test":
		# unittest tries to read sys.argv. :(
		import sys
		sys.argv = sys.argv[:1]
		unittest.main()
		return


def get_options(args):
	parser = argparse.ArgumentParser(prog="mb.py")
	parser.add_argument("--encode", "-e", help="Encode bytes from stdin or files.", 
		dest='mode', action='store_const', const='encode', default='encode'
	)
	parser.add_argument("--decode", "-d", help="Decode bytes from stdin.", 
		dest='mode', action='store_const', const='decode'
	)

	parser.add_argument("--interactive", "-i",
		dest='mode', action='store_const', const='interactive'
	)
	parser.add_argument("--test", help="run unit tests",
		dest='mode', action='store_const', const='test'
	)
	parser.add_argument("files", help="A list of files to zip up. (TODO)", nargs='*')
	return parser.parse_args(args)


def interactive():
	while True:
		i = input(": ")
		if not i: break
		mb = mapper.bytes_to_mojibake(i)
		print(" ", mb)
		b = mapper.mojibake_to_bytes(mb)
		out = b.decode(encoding="utf-8")
		if out == i: continue # nothing to see.
		# else:
		print("ERROR! got: ", i)
		print()

def encode_stdin():
	"""Read bytes from stdin, output characters to stdout."""
	stdin = sys.stdin.buffer # (The underlying *binary* buffer)
	output = mapper.encode(data_generator(stdin))
	for mb in output: print(mb, end="")
	print("")

def decode_stdin():
	"""Read characters from stdin, output bytes to stdout."""
	stdin = sys.stdin # (characters)
	stdin = data_generator(stdin)
	# Clean stdin of extra characters (\n, \r, whitespace?)
	stdin = filter_ok_chars(stdin)

	stdout = sys.stdout.buffer # binary
	output = mapper.decode(stdin)
	for data in output: 
		stdout.write(data)


OK_CHARS = "\n\r. "

def filter_ok_chars(data_gen):
	"Remove some extra characters that might show up in stdin strings"
	for data in data_gen:
		for c in OK_CHARS:
			data = data.replace(c, '')
		# If we haven't removed everything:
		if data: yield data



def data_generator(data_file, chunk_bytes=4096):
	"""Continually read from a file and yield bytes objects."""
	while True: 
		data = data_file.read(chunk_bytes)
		if len(data) == 0: break # EOF
		#else:
		yield data



class MultiRange:
	"""A range-like object that joins a multiple disjoint ranges."""

	def __init__(self, ranges):
		self.__ranges = ranges

	def __len__(self):
		return sum([len(r) for r in self.__ranges])

	def index(self, item):
		offset = 0
		for r in self.__ranges:
			if item in r: return offset + r.index(item)
			# else:
			offset += len(r)
		raise ValueError("{} is not in range".format(item))

	def __getitem__(self, i):
		for r in self.__ranges:
			if i < len(r): return r[i]
			else: i -= len(r)
		raise IndexError("range object index ({}) out of range".format(i));

	
class Mapper:
	"""Maps a number into a set of ranges of numbers."""

	characters = MultiRange([
		# http://en.wikipedia.org/wiki/Unicode_block
		# CJK Unified Ideographs Extension B
		range(0x20000, 0x2A6E0),
		# CJK Unified Ideographs
		range(0x4E00, 0xA000),
		# Hangul Syllables
		range(0xAC00, 0xD7B0),
	])

	# For odd numbers of bytes, the last (single) byte will
	# be encoded in the 256 values above 2^16:
	single_byte_offset = 0x10000

	def bytes_to_mojibake(self, b):
		if type(b) is str:
			b = b.encode()

		out = ""
		while b:
			(head, b) = (b[:2], b[2:])
			if len(head) == 2: offset = (head[0] << 8) | head[1]
			else: offset = self.single_byte_offset + head[0] 
			out += chr(self.characters[offset])

		return out

	def encode(self, data_gen):
		"""Yield strings for each bit of data generated by data_gen. (Streaming API)"""
		remainder = bytes()

		for data in data_gen:
			# If we have odd numbers of bytes, save one for the next chunk:
			if remainder: (data, remainder) = (remainder + data, bytes())
			if len(data) % 2 != 0: (data, remainder) = (data[:-1], data[-1:])
			yield self.bytes_to_mojibake(data)

		if remainder:
			yield self.bytes_to_mojibake(data)

	def decode(self, data_gen):
		"""Yield bytes (sequences) for each string yielded by data_gen."""
		for mb in data_gen:
			yield self.mojibake_to_bytes(mb)



	def mojibake_to_bytes(self, mb):
		"""Given mojibake string 'mb', return a bytearray of the data it contains."""
		out = bytearray()
		for c in mb:
			offset = self.characters.index(ord(c))
			if offset >= self.single_byte_offset:
				out.append(offset & 0xFF)
			else:
				out.append(offset >> 8)
				out.append(offset & 0xFF)
		return out


mapper = Mapper()



class MojibakeTests(unittest.TestCase):

	def test_enough_bytes(self):
		# We need at least 2^16 code points for 2-byte representations
		# and an extra 2^8 for one-byte representations.
		min_size = 0x10100

		self.assertTrue(len(mapper.characters) >= min_size)

	# TODO: Mapper.characters should be a 1:1 mapping.


if __name__ == "__main__":
	main(sys.argv[1:])