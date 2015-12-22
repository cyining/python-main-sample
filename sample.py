#!/usr/bin/env python
"""Python sample application
2015'12/20 by Cherng-Ying Ing <cying.ing@gmail.com>
Usage: %s [options]
Options:
"""

def main(argv):
	from getopt import getopt
	topts = []
	topts += [("h", "Show help")]
	sopts = "".join(x for x, _ in topts)
	opts, args = getopt(argv[1:], sopts)
	def _init(sel_sopt, val_type=int):
		for sopt, text in topts:
			if sel_sopt == sopt[0] and sopt[-1:] == ":":
				l, r = text.rfind("("), text.rfind(")")
				if l >= 0 and l < r:
					return val_type(text[l+1:r])
	show_help = False
	if not args:
		show_help = True
	for k, v in opts:
		if k == "-h":
			show_help = True
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
	return 0

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
