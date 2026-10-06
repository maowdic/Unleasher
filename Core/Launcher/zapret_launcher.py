from subprocess import check_output, DEVNULL, run, Popen
from Core.Data.data_manager import DataManager
from os.path import abspath
from typing import Any

class Launcher:
    def __init__(self) -> None:
        self.__data_manager: DataManager = DataManager()
        self.__LAUNCHER_PATH: str = abspath(f"{self.__data_manager.UNPACKED_FOLDER_PATH}zapret\\zapret_launcher.cmd")
        self.__TASKNAME: str = "zapret_launched_by_Unleasher"
        
    def SilentLaunch(self, command: Any, easy_task: bool = True) -> None:
        function: Any = run if easy_task else Popen
        function(
            command,
            creationflags=0x08000000,
            stderr=DEVNULL,
            stdout=DEVNULL
        )

    def ChangeLaunchStatus(self, activate: bool) -> None:
        if activate:
            self.SilentLaunch(["cmd.exe", "/c", self.__LAUNCHER_PATH], False)
            return
        
        if self.CheckIfZapretIsRunning():
            for command in [["taskkill", "/F", "/IM", "winws.exe"], ["sc", "stop", "WinDivert"]]:
                self.SilentLaunch(command)

    def CheckIfZapretIsRunning(self) -> bool:
        return "winws.exe" in check_output("tasklist", text=True, creationflags=0x08000000).lower()

    def ChangeAutoloaderStatus(self, activate: bool) -> None:
        self.SilentLaunch(["schtasks", "/Create", "/TN", self.__TASKNAME, "/TR", self.__LAUNCHER_PATH, "/SC", "ONLOGON", "/RL", "HIGHEST", "/RU", "SYSTEM", "/F"]
        if activate else ["schtasks", "/Delete", "/TN", self.__TASKNAME, "/F"])