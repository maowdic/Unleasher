import sys
from os import environ
from os.path import exists
from typing import Any
from json import load, dump
from shutil import copytree

class DataManager:
    def __init__(self: Any) -> None:
        self.__DEFAULT_DATA: dict[str, bool] = {
            "active" : False,
            "autoloader" : False,
            "setting": "general (ALT9).bat",
            "version": "1.10.3",
        }
        self.__FILENAME: str = "local_data.json"
        self.UNPACKED_FOLDER_PATH: str = f"{environ["APPDATA"]}\\Unleasher\\"

    def ExtractData(self: Any, filepath: str = "local_data.json") -> dict[str, bool] | list[str] | None:
        try:
            with open(self.UNPACKED_FOLDER_PATH+filepath) as file:
                return load(file)
        except FileNotFoundError:
            if filepath != self.__FILENAME:
                return
            self.InsertData(reset=True)
            return self.__DEFAULT_DATA

    def InsertData(self: Any, key: Any = None, value: Any = None, reset: bool = False) -> None:
        current_data: dict = self.__DEFAULT_DATA if reset else self.ExtractData()
        if not reset:
            current_data[key] = value

        with open(self.UNPACKED_FOLDER_PATH+self.__FILENAME, "w") as file:
            dump(current_data, file, indent=4)

    def UnpackData(self: Any) -> bool:
        if not exists(self.UNPACKED_FOLDER_PATH):
            copytree(f"{sys._MEIPASS}\\Binaries", f"{self.UNPACKED_FOLDER_PATH}")
            return True
        return False