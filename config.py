import toml


class Config:
    def __init__(self, config_file="config.toml"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        return toml.load(self.config_file)

    def save_config(self):
        with open(self.config_file, "w") as f:
            toml.dump(self.config, f)

    def set_cookies(self, cookies):
        self.config["qzone"]["COOKIES"] = cookies
        self.save_config()

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
        self.save_config()


config = Config()

WORKDIR = config["project"]["WORKDIR"]
FILE = config["project"]["FILE"]
AUTO_SAVE = config["project"]["AUTO_SAVE"]
AUTO_SAVE_DIR = config["project"]["AUTO_SAVE_DIR"]
STEP = config["project"]["STEP"]
LIMIT = config["project"]["LIMIT"]
SLEEP_TIME = config["project"]["SLEEP_TIME"]
MAX_RETRY = config["project"]["MAX_RETRY"]
SEARCH_OFFSET = config["project"]["SEARCH_OFFSET"]

USER = config["qzone"]["USER"]
PASS = config["qzone"]["PASS"]
UIN = config["qzone"]["UIN"]
NICKNAME = config["qzone"]["NICKNAME"]
COOKIES = config["qzone"]["COOKIES"]

USE_GPU = config["paddleocr"]["USE_GPU"]
USE_MP = config["paddleocr"]["USE_MP"]
TOTAL_PROCESS_NUM = config["paddleocr"]["TOTAL_PROCESS_NUM"]
