import aiohttp
import asyncio
import io
import logging
import numpy as np
from config import AUTO_SAVE, AUTO_SAVE_DIR
from PIL import Image
from paddleocr import PaddleOCR
from qzone_dump import read_messages, write_messages


ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="ch",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
)

logger = logging.getLogger("ppocr")
logger.setLevel(logging.INFO)


def recognize_text(img_array):
    result = ocr.predict(input=img_array)
    if not result or len(result) == 0:
        return None
    text_lines = []
    for res in result:
        if 'rec_texts' in res:
            text_lines.extend(res['rec_texts'])
    return text_lines if text_lines else None


async def ocr_message(session, message):
    for index, picture_url in enumerate(message["pictures"]):
        async with session.get(picture_url) as resp:
            img = await resp.read()
            if resp.headers["Content-Type"] == "image/gif":
                img_byte_arr = io.BytesIO()
                Image.open(io.BytesIO(img)).save(img_byte_arr, format="PNG")
                img = img_byte_arr.getvalue()

            img_obj = Image.open(io.BytesIO(img)).convert("RGB")
            img_array = np.ascontiguousarray(np.array(img_obj))
            try:
                ocr_result = recognize_text(img_array)
            except Exception as e:
                logger.exception("OCR failed for image %s: %s", picture_url, e)
                continue

            if ocr_result is None or len(ocr_result) == 0:
                continue

            ocr_text = "".join(ocr_result).strip()
            if len(ocr_text) > 0:
                message["ocr"] += f"P{index + 1}: "
                message["ocr"] += ocr_text
                message["ocr"] += "\n"


async def ocr_messages():
    messages = read_messages()
    print("OCRing messages...")
    async with aiohttp.ClientSession() as session:
        count = 0
        for message in messages:
            if message["ocr"] is not None:
                continue
            elif len(message["pictures"]) > 0:
                print(count, end=": ")
                message["ocr"] = ""
                await ocr_message(session, message)
                print(f"OCRed message {message['tid']}.")
                if AUTO_SAVE > 0 and count % AUTO_SAVE == 0:
                    write_messages(messages, AUTO_SAVE_DIR)
                count += 1
            else:
                print(count, end=": ")
                message["ocr"] = ""
                print(f"Message {message['tid']} has no pictures.")

    write_messages(messages)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocr_messages())
