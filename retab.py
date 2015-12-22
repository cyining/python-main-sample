#!/usr/bin/env python
"""Python code re-tab tool
2015'12/20 by Cherng-Ying Ing <cying.ing@gmail.com>
Usage: %s [options] <input-file-name> [output-file-name]
Options:
"""
import os
import os.path
import re

def frame_suffix(fname, suffix="", ext=".py"):
	fbase, fext = os.path.splitext(fname)
	if not fext or fext.lower() != ext:
		fext += ext
	return fbase + suffix + fext

def str_ranges(nums):
	msg = ""
	first = last = None
	def token():
		sep = ""
		if msg:
			sep = " "
		if first == last:
			return sep + "%d" % first
		return sep + "%d~%d" % (first, last)
	for num in nums:
		if last == None:
			first = last = num
			continue
		if num == last + 1:
			last += 1
			continue
		msg += token()
		first = last = None
	if last != None:
		msg += token()
	return msg

def main(argv):
	from getopt import getopt
	topts = []
	topts += [("h", "Show help")]
	topts += [("d", "Disable smart doc string processing")]
	topts += [("t:", "Treat each existing tab as <n> spaces")]
	topts += [("n:", "Convert <n> spaces to one tab (4)")]
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
	smart_doc = True
	tab_space = 0
	space_tab = _init("n")
	move_dir, move_ext = None, None
	if not args:
		show_help = True
	for k, v in opts:
		if k == "-h":
			show_help = True
		elif k == "-d":
			smart_doc = False
		elif k == "-t":
			tab_space = int(v)
			if tab_space not in range(9):
				print("-t accept values between 1~8")
				return 2
		elif k == "-n":
			space_tab = int(v)
			if space_tab not in range(9):
				print("-n accept values between 1~8")
				return 2
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
	ofp = open(ofname, "wt")
	rp_indent = re.compile("^[ \t]+")
	doc_strs = ('"' * 3, "'" * 3)
	in_doc = None
	tab_lines = []
	space_lines = []
	issue_lines = []
	line_no = 0
	for line in ifp:
		line_no += 1
		ndoc = sum([line.count(x) for x in doc_strs])
		indent = ""
		r = rp_indent.search(line)
		if r:
			indent = r.group(0)
			remain = line[r.end():]
		if smart_doc and in_doc:
			if in_doc[0] and in_doc[0] == indent[:len(in_doc[0])]:
				indent = in_doc[1] + indent[len(in_doc[0]):]
		else:
			if "\t" in indent:
				if tab_space:
					indent = indent.replace("\t", " " * tab_space)
				else:
					tab_lines += [line_no]
			indent = indent.replace(" " * space_tab, "\t")
		if indent:
			if "\t" in indent and indent[-1:] == " ":
				space_lines += [line_no]
			if " \t" in indent:
				issue_lines += [line_no]
			line = indent + remain
		if ndoc & 1:
			if in_doc:
				in_doc = None
			elif r:
				in_doc = (r.group(0), indent)
			else:
				in_doc = ("", "")
		ofp.write(line)
	ifp.close()
	ofp.close()
	if tab_lines:
		print("* Lines with existing tabs: (Consider use -t)")
		print("  " + str_ranges(tab_lines))
	if space_lines:
		print("* Lines with spaces left:")
		print("  " + str_ranges(space_lines))
	if issue_lines:
		print("* Lines with spaces 'in the middle' left:")
		print("  " + str_ranges(issue_lines))
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
