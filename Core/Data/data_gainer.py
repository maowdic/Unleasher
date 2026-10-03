from typing import Any
from json import loads
from requests import get
from os.path import abspath
from Core.Data.data_manager import DataManager
from Core.Launcher.zapret_launcher import Launcher

class DataGainer:
    def __init__(self: Any) -> None:
        self.__DATA_MANAGER: DataManager = DataManager()
        self.__ZAPRET_LAUNCHER: Launcher = Launcher()
        self.__DATA_TABLE: dict[str, str] = {
            "%BIN%" : abspath(f"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}zapret\\executable") + "\\",
            "%LISTS%" : abspath(f"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}zapret\\lists") + "\\",
            "%GameFilterTCP%": "1024-65535",
            "%GameFilterUDP%": "1024-65535",
            " ^\n": "",
            "-user": ""
        }
        pass

    def UpdateSettings(self: Any, file_name: str = "general (EXP)") -> bool:
        file_name += ".bat"
        was_activated: bool = self.__DATA_MANAGER.ExtractData()["active"]

        try:
            settings_raw: str = get("https://raw.githubusercontent.com/Flowseal/zapret-discord-youtube/refs/heads/main/" + file_name).content.decode("utf-8")
            
            for old, new in self.__DATA_TABLE.items():
                settings_raw = settings_raw.replace(old, new, -1)
            
            settings: list[str] = settings_raw.split("--")[1:]
            self.__DATA_MANAGER.InsertData("setting", file_name)

            if was_activated:
                self.__ZAPRET_LAUNCHER.ChangeLaunchStatus(False)

            with open(f"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}zapret\\zapret_launcher.cmd", "w", encoding="utf-8") as file:
                file.write(f"chcp 65001 > nul\ncd /d \"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}zapret\\executable\"\nwinws.exe --{" --".join(settings)}")

            if was_activated:
                self.__ZAPRET_LAUNCHER.ChangeLaunchStatus(True)
        except:
            return False
        return True

    def GetSettings(self: Any) -> list[str]:
        settings_list: list[str] = []

        for i in loads(get("https://api.github.com/repos/Flowseal/zapret-discord-youtube/contents?ref=main").content.decode("utf-8")):
            setting_name: str = i['name']
            if "general" in setting_name:
                settings_list.append(setting_name[:-4])

        return settings_list