#!/usr/bin/env python3
"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load("stack.ls8")
# cpu.load(stack.ls8)
cpu.run()