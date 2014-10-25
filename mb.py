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

	def mojibake_to_bytes(self, mb):
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