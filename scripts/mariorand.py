import sys
import binascii
import re

def _ror(val, carry):
	next_carry	= bool(val & 1)
	val			= (val >> 1)
	if carry:
		val |= 0x80
	return val, next_carry

def random_init():
	return [ 0xA5 ] + ([ 0 ] * 6)

def random_advance(seed):
	carry = bool((seed[0] & 0x02) ^ (seed[1] & 0x02))

	for i in range(0, len(seed)):
		seed[i], carry = _ror(seed[i], carry)

	return seed

find = [ ]
#FRAMERULE_FRAMES=21 # NTSC
FRAMERULE_FRAMES=18 # PAL

def generate_quick_resume():
	seed = random_init()
	for base_i in range(0, 5):
		base = base_i * 32
		print("quick_resume_" + str(base) + ":")
		for i in range(0, 32):
			rngbase = (base + i)  * 100
			print('	.byte ' + ', '.join('${:02x}'.format(x) for x in seed) + ', $00 ; Base for ' + str(rngbase))
			if rngbase >= 9900:
				exit(0)
			for u in range(0, (100 * FRAMERULE_FRAMES)):
				seed = random_advance(seed)


def locate_seed_frame(needle):
	needle_ary = list(map(int, bytearray.fromhex(re.sub("[^0-9a-fA-F]", "", needle))))
	seed = random_init()
	for i in range(0, 100000):
		seed = random_advance(seed)
		if seed != needle_ary:
			continue
		rule = int(i / FRAMERULE_FRAMES)
		off = int(i % FRAMERULE_FRAMES)
		print('found on frame: %d, framerule: %d, framerule offset: %d' % (i, rule, off))


#generate_quick_resume()
locate_seed_frame("E9E635F9926145")
