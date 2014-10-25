#!/usr/bin/env python3

from random import randint

def main(args):
	print("Mapper count:", mapper.count)

	while True:
		i = input()
		if not i: break
		show(i)

def show(m):
	print(m)
	print(bytes_to_mojibake(m))




def bytes_to_mojibake(b):
	if type(b) is str:
		b = b.encode()

	out = ""
	while b:
		(head, b) = (b[:2], b[2:])
		if len(head) == 1:
			out += "="
			head = bytes([0]) + head
		l = (head[0] << 8) | head[1]
		out += chr(mapper.map_into(l))

	return out



def chunk(seq, size=2):
	if len(seq) == 0:
		yield []
		return
	# else:
	while seq:
		(head, seq) = (seq[:size], seq[size:])
		yield head
	


	
class Mapper:
	"""Maps a number into a set of ranges of numbers."""

	ranges = [
		# http://en.wikipedia.org/wiki/Unicode_block
		# CJK Unified Ideographs Extension B
		range(0x20000, 0x2A6E0),
		# CJK Unified Ideographs
		range(0x4E00, 0xA000),
		# Hangul Syllables
		range(0xAC00, 0xD7B0),
	]

	@property 
	def count(self):
		count = 0
		for r in self.ranges:
			print(len(r))
			count += len(r)
		return count

	def map_into(self, num):
		for r in self.ranges: 
			if num < len(r): return r[num]
			else: num -= len(r)
		raise Exception("Can't map_into({}}".format(num))

	def map_outof(self, num):
		offset = 0
		for r in self.ranges:
			if num in r: return offset + (num - r.start)
			else: offset += len(r)
		raise Exception("Can't map_outof({}}".format(num))

mapper = Mapper()

if __name__ == "__main__":
	import sys
	main(sys.argv[1:])