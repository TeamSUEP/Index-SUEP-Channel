import argparse
import asyncio
import os
import time
from qzone_dump import dump_messages
from render_data import render_messages, render_index
from separate_messages import split_year


parser = argparse.ArgumentParser()
parser.add_argument("--new", action="store_true")
parser.add_argument("--old", action="store_true")
args = parser.parse_args()

count = dump_messages(dump_new=args.new, dump_old=args.old)

if count > 0:
    from qzone_dump_img_ocr import ocr_messages

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocr_messages())
    current_year = time.strftime("%Y", time.localtime())
    split_year(f"dist/data/years/{current_year}.json", "dist/data/months", current_year)
    render_messages()
    render_index()

if "GITHUB_OUTPUT" in os.environ:
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"messagesAdded={count}\n")
