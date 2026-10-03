import ctypes
from Core.gui import App

if __name__ == "__main__":
    if not(ctypes.windll.shell32.IsUserAnAdmin()):
        ctypes.windll.user32.MessageBoxW(0, "Пожалуйста, запустите программу с правами администратора!", "Запущено не с правами администратора!", 0x40)
    else:
        App().Launch()