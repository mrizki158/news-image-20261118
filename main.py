"""news-image-20261118 entry: copy the day's news image to /output/entry.png.

The image beside this file (entry.png) sums up the world news of Wednesday
18 November 2026. The grader runs this program twice with no network; both
runs must write the same bytes, so the program is a pure copy.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT_DIR, "entry.png"))
