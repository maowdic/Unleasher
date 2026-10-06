import sys
from os import environ
from os.path import exists
from typing import Any
from json import load, dump
from shutil import copytree

class DataManager:
    def __init__(self) -> None:
        self.__DEFAULT_DATA: dict[str, bool] = {
            "active" : False,
            "autoloader" : False,
            "setting": "general (ALT9).bat",
            "version": "1.10.3",
        }
        self.__FILENAME: str = "local_data.json"
        self.UNPACKED_FOLDER_PATH: str = f"{environ["APPDATA"]}\\Unleasher\\"

    def ExtractData(self, key: str) -> Any:
        try:
            with open(self.UNPACKED_FOLDER_PATH + self.__FILENAME) as file:
                return load(file)[key]
        except FileNotFoundError:
            self.InsertData(reset=True)
            return self.__DEFAULT_DATA
        except KeyError:
            default_data: Any = self.__DEFAULT_DATA[key]
            self.InsertData(key, default_data)
            return default_data

    def InsertData(self, key: Any = None, value: Any = None, reset: bool = False) -> None:
        with open(self.UNPACKED_FOLDER_PATH + self.__FILENAME) as file:
            if not reset:
                loaded_file: dict[str, Any] = self.TryToLoad(file) or self.__DEFAULT_DATA
                loaded_file[key] = value
        
        with open(self.UNPACKED_FOLDER_PATH + self.__FILENAME, "w+") as file:
            dump(self.__DEFAULT_DATA if reset else loaded_file, file, indent=4)

    def UnpackData(self) -> bool:
        if not exists(self.UNPACKED_FOLDER_PATH):
            copytree(f"{sys._MEIPASS}\\Binaries", f"{self.UNPACKED_FOLDER_PATH}")
            return True
        return False

    def TryToLoad(self, file_object: Any) -> None | dict[str, Any]:
        try: return load(file_object)
        except: return None