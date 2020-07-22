#!/usr/bin/env python3

"""Main."""

# import sys
# from cpu import *

# cpu = CPU()

# cpu.load(sys.argv[1])
# cpu.run()

import sys
from os.path import join
from cpu import *
# filename = sys.argv[1]
filename = open(join('./examples/', sys.argv[1]), 'r')
code = filename.readlines()
filename.close()
cpu = CPU()
cpu.load(code)