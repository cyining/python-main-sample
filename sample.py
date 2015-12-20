#!/usr/bin/env python
"""Python sample application
2015'12/20 by Cherng-Ying Ing <cying.ing@gmail.com>
Usage: %s [options]
Options:
"""

def main(argv):
	from getopt import getopt
	sopts = ""
	opts, args = getopt(argv[1:], sopts)
	show_help = False
	if not args:
		show_help = True
	for k, v in opts:
		pass
	if show_help:
		print(__doc__ % argv[0])
		return 1
	return 0

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
