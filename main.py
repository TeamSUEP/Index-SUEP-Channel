import argparse
import asyncio
import os
from qzone_dump import dump_messages
from qzone_dump_img_ocr import ocr_messages
from render_data import render_messages, render_index

parser = argparse.ArgumentParser()
parser.add_argument("--new", action="store_true")
parser.add_argument("--old", action="store_true")
args = parser.parse_args()

count = dump_messages(dump_new=args.new, dump_old=args.old)
if count > 0:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocr_messages())
    render_messages()
    render_index()

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"messagesAdded={count}\n")
