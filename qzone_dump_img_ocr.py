import aiohttp
import asyncio
import io
import logging
from config import AUTO_SAVE, AUTO_SAVE_DIR, USE_GPU, USE_MP, TOTAL_PROCESS_NUM
from PIL import Image
from paddleocr import PaddleOCR
from qzone_dump import read_messages, write_messages


ocr = PaddleOCR(
    use_angle_cls=True,
    lang="ch",
    use_gpu=USE_GPU,
    use_mp=USE_MP,
    total_process_num=TOTAL_PROCESS_NUM,
)

logger = logging.getLogger("ppocr")
logger.setLevel(logging.INFO)


def recognize_text(img):
    return ocr.ocr(img, cls=True)[0]


async def ocr_message(session, message):
    for index, picture_url in enumerate(message["pictures"]):
        async with session.get(picture_url) as resp:
            img = await resp.read()
            if resp.headers["Content-Type"] == "image/gif":
                img_byte_arr = io.BytesIO()
                Image.open(io.BytesIO(img)).save(img_byte_arr, format="PNG")
                img = img_byte_arr.getvalue()
            ocr_result = recognize_text(img)
            if ocr_result is None:
                continue
            ocr_result = "".join([line[1][0] for line in ocr_result]).strip()
            if len(ocr_result) > 0:
                message["ocr"] += f"P{index + 1}: "
                message["ocr"] += ocr_result
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
