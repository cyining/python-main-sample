#!/usr/bin/env python
"""Text line ending reformat tool
2015'12/20 by Cherng-Ying Ing <cying.ing@gmail.com>
Usage: %s [options] <input-file-name> [output-file-name]
Options:
"""
import os
import os.path

def tail_cut(line, tail_chrs):
	"""
	Cut a line from where the leading part have no tailing characters

	- line: input line string
	- tail_chrs: tailing characters

	Return a tuple containing the leading and tailing parts
	"""
	size = len(line)
	for i in range(size-1, -1, -1):
		if line[i] not in tail_chrs:
			cut = i + 1
			return line[:cut], line[cut:]
	return "", line

crlf_chrs = "\r\n"
tail_chrs = " \t"

def frame_suffix(fname, suffix="", ext=""):
	fbase, fext = os.path.splitext(fname)
	if not fext or fext.lower() != ext:
		fext += ext
	return fbase + suffix + fext

def main(argv):
	from getopt import getopt
	topts = []
	topts += [("h", "Show help")]
	topts += [("t", "Strip tailing white-space (False)")]
	topts += [("d", "Apply DOS style line ending (False)")]
	topts += [("o", "Generate output file (False)")]
	topts += [("i:", "Convert inplace and move original to <d:e>")]
	sopts = "".join(x for x, _ in topts)
	opts, args = getopt(argv[1:], sopts)
	def _init(sel_sopt, val_type=int):
		for sopt, text in topts:
			if sel_sopt == sopt[0] and sopt[-1:] == ":":
				l, r = text.rfind("("), text.rfind(")")
				if l >= 0 and l < r:
					return val_type(text[l+1:r])
	show_help = False
	strip_tail = _init("t")
	dos_style = _init("d")
	output = _init("o")
	move_dir, move_ext = None, None
	if not args:
		show_help = True
	for k, v in opts:
		if k == "-h":
			show_help = True
		elif k == "-t":
			strip_tail = True
		elif k == "-d":
			dos_style = True
		elif k == "-o":
			output = True
		elif k == "-i":
			if v.count(":") != 1:
				print("-i require format 'dir:ext'")
				return 2
			move_dir, move_ext = v.split(":")
			if not move_dir and not move_ext:
				print("-i <dir:ext> require either 'dir' or 'ext' non-empty")
				return 2
			if move_dir and not os.path.isdir(move_dir):
				print("Directory not exist: %s" % move_dir)
				return 2
			if move_ext and not "." in move_ext:
				move_ext = "." + move_ext
	if show_help:
		def _help(sopt, text):
			v = ""
			if sopt[-1:] == ":":
				v = "x"
				l, r = text.find("<"), text.find(">")
				if l >= 0 and l < r:
					v = " " + text[l+1:r]
			return "\t-" + sopt[0] + v + "\t" + text + "\n"
		print(__doc__ % argv[0] + "".join(_help(*x) for x in topts))
		return 1
	ifname = frame_suffix(args[0])
	if not os.path.exists(ifname):
		print("Input file not found: %s" % ifname)
		return 2
	if len(args) > 1:
		ofname = frame_suffix(args[1])
	else:
		ofname = frame_suffix(ifname, "_o")
	if ifname.lower() == ofname.lower():
		print("Input and output files must be different")
		return 2
	ending = "\n"
	if dos_style:
		ending = "\r\n"
	counts = {"\n": 0, "\r\n": 0}
	std_counts = counts.keys()
	tail_count = 0
	ifp = open(ifname, "rt")
	if output:
		ofp = open(ofname, "wt")
	for line in ifp:
		text, crlf = tail_cut(line, crlf_chrs)
		#print(repr((text, crlf)))
		if crlf not in counts:
			counts[crlf] = 0
		counts[crlf] += 1
		head, tail = tail_cut(text, tail_chrs)
		if tail:
			#print(repr((text, tail, crlf)))
			tail_count += 1
		if output:
			line = text
			if strip_tail:
				line = head
			line += ending
			ofp.write(line)
	ifp.close()
	if output:
		ofp.close()
	totals = []
	for k in std_counts:
		v = counts[k]
		if v:
			totals.append('%s:%d' % (repr(k), v))
	odd = len(counts) - len(std_counts)
	if odd:
		totals.append('odd:%d' % odd)
	for k, v in counts.items():
		if k not in std_counts:
			totals.append('%s:%d' % (repr(k), v))
	if tail_count:
		totals.append('tail:%d' % tail_count)
	print('%s %s' % (ifname, ' '.join(totals)))
	if move_dir or move_ext:
		nfname = ifname
		if move_dir:
			nfname = os.path.join(move_dir, os.path.basename(nfname))
		if move_ext:
			nfname += move_ext
		os.rename(ifname, nfname)
		os.rename(ofname, ifname)
		print("Convert inplace and backup to %s" % nfname)
	return 0

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
