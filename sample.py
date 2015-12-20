#!/usr/bin/env python
"""Python sample application
2015'12/20 by Cherng-Ying Ing <cying.ing@gmail.com>
Usage: %s [options] <output-file-name>
Options:
"""

def main(argv):
	from getopt import getopt
	topts = []
	topts += [("h", "Show help")]
	topts += [("t:", "Output each tab as <n> spaces")]
	sopts = "".join(x for x, _ in topts)
	opts, args = getopt(argv[1:], sopts)
	show_help = False
	tab_space = 0
	if not args:
		show_help = True
	for k, v in opts:
		if k == "-h":
			show_help = True
		elif k == "-t":
			tab_space = int(v)
			if tab_space not in range(9):
				print("-t accept values between 1~8")
				return 2
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
	ofname = args[0]
	ifname = argv[0]
	if "." not in ofname or ofname[-3:] != ".py":
		ofname += ".py"
	from os.path import basename
	if ofname.lower() == basename(ifname).lower():
		print("Only accept file name other than %s" % ifname)
		return 2
	ifp = open(ifname, "rt")
	ofp = open(ofname, "wt")
	for line in ifp:
		if tab_space:
			line = line.replace("\t", " " * tab_space)
		ofp.write(line)
	ifp.close()
	ofp.close()
	return 0

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
