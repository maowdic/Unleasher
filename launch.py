import ctypes
from Core.gui import App
from sys import (argv, executable,
                exit as Sexit)

if __name__ == "__main__":
    if not(ctypes.windll.shell32.IsUserAnAdmin()):
        if ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, " ".join(argv), None, 1) <= 32:
            ctypes.windll.user32.MessageBoxW(0,
                "Пожалуйста, запустите программу с правами администратора!",
                "UNLEASHER - отказано в доступе.", 0x10)
        Sexit(0)
    
    App().Launch()