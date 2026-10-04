from typing import Any
from Core.Data.data_gainer import DataGainer
from Core.Data.data_manager import DataManager
from Core.Launcher.zapret_launcher import Launcher
from flet import (Page, run, Text, Switch, Alignment, BorderSide,
                    IconButton, Icons, Column, ButtonStyle, Tooltip,
                    RoundedRectangleBorder as RRB, TextStyle, Colors, MenuStyle,
                    BoxDecoration, Theme, TooltipTheme, Row, Dropdown, DropdownOption)

class App:
    def __init__(self: Any) -> None:
        self.APP_NAME: str = "UNLEASHER"
        self.__DATA_MANAGER: DataManager = DataManager()
        self.__DATA_GAINER: DataGainer = DataGainer()
        self.__LAUNCHER: Launcher = Launcher()
        self.__UPDATE_DOWNLOADED: bool = True
        self.__COLORS: dict[str] = {
            "default": "#F5F5DC",
            "green": "#00A700",
            "red": "#A70000"
        }
        self.__OPTIONS: list[str] = self.__DATA_GAINER.GetSettings()

    def __Body(self: Any, page: Page) -> None:
        page.theme = Theme(
            tooltip_theme=TooltipTheme(
                decoration=BoxDecoration(bgcolor="dark"), 
                text_style=TextStyle(color=self.__COLORS["default"], size=10))
            )

        page.theme_mode = "dark"
        page.title = self.APP_NAME
        page.window.width = 385
        page.window.height = 455
        page.window.resizable = False
        page.window.maximizable = False

        page.fonts = {"Banner": f"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}flet\\Font.ttf"}
        page.window.icon = f"{self.__DATA_MANAGER.UNPACKED_FOLDER_PATH}flet\\AppIcon.ico"

        def AutoloaderAction() -> None:
            self.__DATA_MANAGER.InsertData("autoloader", AUTOLOADER.value)
            AUTOLOADER.track_outline_color = ChangeColor("autoloader")
            self.__LAUNCHER.ChangeAutoloaderStatus(AUTOLOADER.value)

        def LaunchAction() -> None:
            current_state: bool = not(self.__DATA_MANAGER.ExtractData()["active"])
            self.__DATA_MANAGER.InsertData("active", current_state)
            LAUNCH.style.shape.side.color = ChangeColor()
            LAUNCH.tooltip = ChangeTooltip()
            self.__LAUNCHER.ChangeLaunchStatus(current_state)

        def Update() -> None:
            if not(self.__UPDATE_DOWNLOADED):
                return
            self.__UPDATE_DOWNLOADED = False
            download_response: bool = self.__DATA_GAINER.UpdateSettings(file_name=VERSION.value)
            self.__UPDATE_DOWNLOADED = True
            UPDATE.style.shape.side.color = self.__COLORS["green" if download_response else "red"]
            UPDATE.tooltip = Tooltip("Обновление прошло успешно." if download_response else "Произошла ошибка скачивания.",
                vertical_offset=50)

        def ChangeColor(param: str = "active") -> str:
            return self.__COLORS["green" if self.__DATA_MANAGER.ExtractData()[param] else "red"] 

        def ResetUpdate() -> None:
            UPDATE.style.shape.side.color = self.__COLORS["default"]
            UPDATE.tooltip=Tooltip("Обновить настройки подключения.", vertical_offset=50)
        
        def ChangeTooltip() -> Tooltip:
            return Tooltip("Служба обхода активна." if self.__DATA_MANAGER.ExtractData()["active"] else "Служба обхода неактивна.",
            vertical_offset=82.5, text_style=TextStyle(color=self.__COLORS["default"], size=10))

        BANNER: Text = Text(self.APP_NAME, align=Alignment.CENTER, size=75, 
            font_family="Banner", color=self.__COLORS["default"])
        
        LAUNCH: IconButton = IconButton(Icons.POWER_SETTINGS_NEW_OUTLINED, icon_size=150, align=Alignment.CENTER,
            style=ButtonStyle(shape=RRB(radius=20, side=BorderSide(width=0.5, color=ChangeColor()))),
            on_click=LaunchAction, icon_color=self.__COLORS["default"], tooltip=ChangeTooltip())

        VERSION: Dropdown = Dropdown(value=self.__DATA_MANAGER.ExtractData()["setting"][:-4], width=150, border_radius=20, border_color=self.__COLORS["default"], 
            border_width=0.5, options=[DropdownOption(text=i, key=i) for i in self.__OPTIONS], align=Alignment.BOTTOM_CENTER, tooltip=Tooltip("Выбор настроек подключения.", vertical_offset=135),
            menu_height=110, menu_style=MenuStyle(shape=RRB(radius=17.5, side=BorderSide(width=0.5, color=self.__COLORS["default"]))), on_select=ResetUpdate)

        UPDATE: IconButton = IconButton(Icons.DOWNLOAD_OUTLINED, icon_size=100, align=Alignment.CENTER, height=100, width=150,
            style=ButtonStyle(shape=RRB(radius=20, side=BorderSide(width=0.5, color=self.__COLORS["default"]))), 
            icon_color=self.__COLORS["default"], tooltip=Tooltip("Обновить настройки подключения.", vertical_offset=50), 
            on_click=Update)
        
        AUTOLOADER: Switch = Switch(value=self.__DATA_MANAGER.ExtractData()["autoloader"], 
            align=Alignment.CENTER, label=" Автозапуск службы обхода блокировок",
            label_text_style=TextStyle(size=13, color=self.__COLORS["default"]),
            tooltip=Tooltip("WinWS.exe будет включаться автоматически при запуске компьютера.", vertical_offset=15),
            on_change=AutoloaderAction, track_outline_color=ChangeColor("autoloader"), 
            track_outline_width=0.5, active_track_color=Colors.GREY_900, autofocus=False,
            inactive_track_color=Colors.GREY_900, thumb_color=self.__COLORS["default"])

        page.add(
            Column([
            BANNER,
            Row([LAUNCH, 
                Column([VERSION, UPDATE])
                ], spacing=15),
            AUTOLOADER
            ], spacing=30))

    def Launch(self: Any) -> None:
        if self.__DATA_MANAGER.UnpackData():
            self.__DATA_GAINER.UpdateSettings()
        run(self.__Body)