import os
import json
import sys
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from datashovel.readers.pdfreader import PdfReader

reader = PdfReader("../input/example/subgraph.pdf")
reader.read()