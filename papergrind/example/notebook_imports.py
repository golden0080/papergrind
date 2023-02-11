import os
import sys

paths = ["../.."]

for p in paths:
    abs_path = os.path.abspath(p)
    if abs_path not in sys.path:
        print(f"adding {abs_path} to sys.path")
        sys.path.append(abs_path)
