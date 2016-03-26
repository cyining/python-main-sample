#!/usr/bin/env python
"""Python sample application
2015'12/20 by Cherng-Ying Ing <cying.ing@gmail.com>
Usage: %s [options] <input-file-name> [output-file-name]
Options:
"""
import os
import os.path

def frame_suffix(fname, suffix="", ext=".py"):
	fbase, fext = os.path.splitext(fname)
	if not fext or fext.lower() != ext:
		fext += ext
	return fbase + suffix + fext

def main(argv):
	from getopt import getopt
	topts = []
	topts += [("h", "Show help")]
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
	output = _init("o")
	move_dir, move_ext = None, None
	if not args:
		show_help = True
	for k, v in opts:
		if k == "-h":
			show_help = True
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
	ifp = open(ifname, "rt")
	if output:
		ofp = open(ofname, "wt")
	for line in ifp:
		if output:
			ofp.write(line)
	ifp.close()
	if output:
		ofp.close()
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
