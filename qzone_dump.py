import json
import toml
import os
import pathlib
import qzone
from dataclasses import dataclass, asdict
from time import sleep
from irregular_spaces import fix_irregular_spaces


@dataclass
class Message:
    tid: str
    content: str
    pictures: list[str]
    video_thumbnails: list[str]
    ctime: int
    ocr: str


config = toml.load("config.toml")
UIN = config["qzone"]["UIN"]
WORKDIR = config["project"]["WORKDIR"]
FILE = config["project"]["FILE"]
STEP = config["project"]["STEP"]
SEARCH_OFFSET = config["project"]["SEARCH_OFFSET"]
LIMIT = config["project"]["LIMIT"]
AUTO_SAVE = config["project"]["AUTO_SAVE"]
AUTO_SAVE_DIR = config["project"]["AUTO_SAVE_DIR"]
SLEEP_TIME = config["project"]["SLEEP_TIME"]
MAX_RETRY = config["project"]["MAX_RETRY"]
COOKIES = config["qzone"]["COOKIES"]

app = qzone.Qzone(**qzone.cookie_str_to_dict(COOKIES))


def check_emotion_loaded(em: qzone.Emotion) -> bool:
    load_list = [
        em.tid,
        em.content,
        em.pictures,
        em.ctime,
        em.origin,
    ]
    load_list += [p for p in em.pictures]
    if em.origin:
        load_list += [em.origin.content]
    return not any([p is qzone.NotLoaded for p in load_list])


def iter_emotions(start: int = 0) -> qzone.Emotion:
    for position in range(start, LIMIT, STEP):
        for emotion in app.emotion_list(uin=UIN, pos=position, num=STEP):
            yield emotion


def dump_emotion(em: qzone.Emotion) -> dict:
    print(f"Dumping {em.tid}...")
    retries = 0
    while retries < MAX_RETRY and not check_emotion_loaded(em):
        em.load()
        retries += 1
    if not check_emotion_loaded(em):
        print(f"Failed to load emotion {em.tid}")
        return {}
    images = [
        p.url.replace("http:", "https:") for p in em.pictures if p.type == "Image"
    ]
    videos = [
        p.url.replace("http:", "https:") for p in em.pictures if p.type == "Video"
    ]
    return asdict(
        Message(
            em.tid,
            em.content + ("\n" + em.origin.content if em.origin else ""),
            images,
            videos,
            em.ctime,
            None if len(images) > 0 else "",
        )
    )


def read_messages(DIR: str = WORKDIR) -> list[dict]:
    messages = []
    if os.path.exists(pathlib.Path(DIR, FILE)):
        messages = json.load(open(pathlib.Path(DIR, FILE)))
    return messages


def write_messages(messages: list[dict], DIR: str = WORKDIR):
    with open(pathlib.Path(DIR, FILE), "w") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)


def sort_messages(messages: list[dict]):
    messages.sort(key=lambda m: m["ctime"], reverse=True)


def deduplicate_messages(messages: list[dict]) -> list[dict]:
    tid_set = set()
    messages_dedup = []
    for m in messages:
        if m["tid"] not in tid_set:
            tid_set.add(m["tid"])
            messages_dedup.append(m)
    return messages_dedup


def fix_messages(messages: list[dict]):
    for m in messages:
        m["content"] = fix_irregular_spaces(m["content"])
        if m["ocr"] is not None:
            m["ocr"] = fix_irregular_spaces(m["ocr"])


def dump_messages(dump_new: bool = True, dump_old: bool = True) -> int:
    messages = read_messages()
    messages_new = []
    messages_old = []
    first_tid = None
    last_tid = None
    count_new = 0
    count_old = 0

    if len(messages) > 0:
        print(f"Found {len(messages)} messages in local storage.")
        first_tid = messages[0]["tid"]
        last_tid = messages[-1]["tid"]
    else:
        print("No messages found in local storage.")

    if dump_new:
        print(f"Dumping new messages before {first_tid}...")
        for emotion in iter_emotions():
            if emotion.tid == first_tid:
                break
            print(count_new, end=": ")
            messages_new.append(dump_emotion(emotion))
            sleep(SLEEP_TIME)
            if AUTO_SAVE > 0 and count_new % AUTO_SAVE == 0:
                write_messages(messages_new + messages, AUTO_SAVE_DIR)
            count_new += 1
        messages = messages_new + messages

    if dump_old:
        print(f"Dumping old messages after {last_tid}...")
        found = False
        for emotion in iter_emotions(len(messages) + SEARCH_OFFSET):
            print(count_old, end=": ")
            if emotion.tid not in [m["tid"] for m in messages]:
                if not found:
                    print(
                        "Could not find links to previous messages, "
                        "please try dumping new messages first."
                    )
                    if input("Continue? [y/N]") != "y":
                        break
                    else:
                        found = True
                messages_old.append(dump_emotion(emotion))
                if AUTO_SAVE > 0 and count_old % AUTO_SAVE == 0:
                    write_messages(messages + messages_old, AUTO_SAVE_DIR)
                count_old += 1
            else:
                print(f"Skipping {emotion.tid}...")
                found = True
            sleep(SLEEP_TIME)

        messages = messages + messages_old

    messages = deduplicate_messages(messages)
    fix_messages(messages)
    sort_messages(messages)
    write_messages(messages)
    return count_new + count_old


if __name__ == "__main__":
    dump_messages(dump_new=True, dump_old=True)
