from subprocess import check_output, DEVNULL, run, Popen
from Core.Data.data_manager import DataManager
from os.path import abspath
from typing import Any

class Launcher:
    def __init__(self: Any) -> None:
        self.__DATA_MANAGER: DataManager = DataManager()
        self.__LAUNCHER_PATH: str = abspath(f"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}zapret\\zapret_launcher.cmd")
        self.__TASKNAME: str = "zapret_launched_by_Unleasher"

    def SilentLaunch(self: Any, command: Any) -> None:
        run(
                command,
                creationflags=0x08000000,
                stderr=DEVNULL,
                stdout=DEVNULL
            )

    def ChangeLaunchStatus(self: Any, activate: bool) -> None:
        if activate:
            Popen(
                [
                    "cmd.exe",
                    "/c",
                    self.__LAUNCHER_PATH
                ],
                creationflags=0x08000000,
                stderr=DEVNULL,
                stdout=DEVNULL
            )
            return
        if "winws.exe" in check_output("tasklist", text=True, creationflags=0x08000000).lower():
            for command in [["taskkill","/F","/IM","winws.exe"], 
                            ["sc", "stop", "WinDivert"]]:
                self.SilentLaunch(command)

    def ChangeAutoloaderStatus(self: Any, activate: bool) -> None:
        self.SilentLaunch(["schtasks", "/Create", "/TN", self.__TASKNAME, "/TR", self.__LAUNCHER_PATH, "/SC", "ONLOGON", "/RL", "HIGHEST", "/RU", "SYSTEM", "/F"]
        if activate else ["schtasks", "/Delete", "/TN", self.__TASKNAME, "/F"])