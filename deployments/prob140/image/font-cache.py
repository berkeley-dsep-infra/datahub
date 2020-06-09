#!/usr/bin/env python

# run matplotlib once to generate the font cache

import os

import matplotlib as mpl
import pylab as plt

mpl.use('Agg')
fig, ax = plt.subplots()
fig.savefig('test.png')

if os.path.exists('test.png'):
	os.remove("test.png")
