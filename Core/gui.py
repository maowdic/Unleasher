from Core.Data.data_gainer import DataGainer
from Core.Data.data_manager import DataManager
from Core.Launcher.zapret_launcher import Launcher
from flet import (Page, run, Text, Switch, Alignment, BorderSide,
                    IconButton, Icons, Column, ButtonStyle, Tooltip, AlertDialog,
                    RoundedRectangleBorder as RRB, TextStyle, Colors, MenuStyle,
                    BoxDecoration, Theme, TooltipTheme, Row, Dropdown, DropdownOption)

class App:
    def __init__(self) -> None:
        self.APP_NAME: str = "UNLEASHER"
        self.__COLORS: dict[str] = {
                    "default": "#F5F5DC",
                    "green": "#00A700",
                    "red": "#A70000"
                }
        self.__data_gainer: DataGainer = DataGainer()
        self.__OPTIONS: list[str] = self.__data_gainer.GetSettings()
        self.__data_manager: DataManager = DataManager()
        self.__zapret_launcher: Launcher = Launcher()
        self.__update_downloaded: bool = True

    def __Body(self, page: Page, show_banner: bool) -> None:
        page.theme = Theme(
            tooltip_theme=TooltipTheme(
                decoration=BoxDecoration(bgcolor="dark"), 
                text_style=TextStyle(color=self.__COLORS["default"], size=10)
                )
        )

        page.theme_mode = "dark"
        page.title = self.APP_NAME
        page.window.width = 385
        page.window.height = 455
        page.window.resizable = False
        page.window.maximizable = False

        page.fonts = {"Banner": f"{self.__data_manager.UNPACKED_FOLDER_PATH}flet\\Font.ttf"}
        page.window.icon = f"{self.__data_manager.UNPACKED_FOLDER_PATH}flet\\AppIcon.ico"

        def AutoloaderAction() -> None:
            self.__data_manager.InsertData("autoloader", autoloader.value)
            autoloader.track_outline_color = ChangeParamColor("autoloader")
            self.__zapret_launcher.ChangeAutoloaderStatus(autoloader.value)

        def LaunchAction() -> None:
            current_state: bool = not(self.__data_manager.ExtractData("active"))
            self.__data_manager.InsertData("active", current_state)
            launch.style.shape.side.color = ChangeParamColor("active")
            launch.tooltip = ChangeTooltip()
            self.__zapret_launcher.ChangeLaunchStatus(current_state)

        def Update() -> None:
            if not(self.__update_downloaded):
                return
            self.__update_downloaded = False
            download_response: bool = self.__data_gainer.UpdateSettings(filename=version.value)
            self.__update_downloaded = True
            update.style.shape.side.color = self.__COLORS["green" if download_response else "red"]
            update.tooltip = Tooltip("Обновление прошло успешно." if download_response else "Произошла ошибка скачивания.",
                vertical_offset=50)

        def ChangeParamColor(param: str) -> str:
            return self.__COLORS["green" if self.__data_manager.ExtractData(param) else "red"] 

        def ResetUpdate() -> None:
            update.style.shape.side.color = self.__COLORS["default"]
            update.tooltip=Tooltip("Обновить настройки подключения.", vertical_offset=50)
        
        def ChangeTooltip() -> Tooltip:
            return Tooltip("Служба обхода активна." if self.__data_manager.ExtractData("active") else "Служба обхода неактивна.",
            vertical_offset=82.5, text_style=TextStyle(color=self.__COLORS["default"], size=10))

        banner: Text = Text(self.APP_NAME, align=Alignment.CENTER, size=75, 
            font_family="Banner", color=self.__COLORS["default"])
        
        launch: IconButton = IconButton(Icons.POWER_SETTINGS_NEW_OUTLINED, icon_size=150, align=Alignment.CENTER,
            style=ButtonStyle(shape=RRB(radius=20, side=BorderSide(width=0.5, color=ChangeParamColor("active")))),
            on_click=LaunchAction, icon_color=self.__COLORS["default"], tooltip=ChangeTooltip())

        version: Dropdown = Dropdown(value=self.__data_manager.ExtractData("setting")[:-4],
            width=150, border_radius=20, border_color=self.__COLORS["default"], border_width=0.5, options=[DropdownOption(text=i, key=i) for i in self.__OPTIONS],
            align=Alignment.BOTTOM_CENTER, tooltip=Tooltip("Выбор настроек подключения.", vertical_offset=135), menu_height=110, 
            menu_style=MenuStyle(shape=RRB(radius=17.5, side=BorderSide(width=0.5, color=self.__COLORS["default"]))), on_select=ResetUpdate)

        update: IconButton = IconButton(Icons.DOWNLOAD_OUTLINED, icon_size=100, align=Alignment.CENTER, height=100, width=150,
            style=ButtonStyle(shape=RRB(radius=20, side=BorderSide(width=0.5, color=self.__COLORS["default"]))), 
            icon_color=self.__COLORS["default"], tooltip=Tooltip("Обновить настройки подключения.", vertical_offset=50), on_click=Update)
        
        autoloader: Switch = Switch(value=self.__data_manager.ExtractData("autoloader"), 
            align=Alignment.CENTER, label=" Автозапуск службы обхода блокировок",
            label_text_style=TextStyle(size=13, color=self.__COLORS["default"]),
            tooltip=Tooltip("WinWS.exe будет включаться автоматически при запуске компьютера.", vertical_offset=15),
            on_change=AutoloaderAction, track_outline_color=ChangeParamColor("autoloader"), 
            track_outline_width=0.5, active_track_color=Colors.GREY_900, autofocus=False,
            inactive_track_color=Colors.GREY_900, thumb_color=self.__COLORS["default"])
        
        page.add(
            Column([
            banner,
            Row([launch, 
                Column([version, update])
                ], spacing=15),
            autoloader
            ], spacing=30))

        if show_banner:
            page.show_dialog(
                AlertDialog(title=Text(f"ZAPRET {self.__data_manager.ExtractData("version")}", align=Alignment.CENTER), 
                title_text_style=TextStyle(size=40, color=self.__COLORS["default"], font_family="Banner"), modal=True,
                content=Text(f"Настоятельно рекомендуем вам обновить настройки подключения!"),
                content_text_style=TextStyle(size=13.5, color=self.__COLORS["default"]), actions=
                [IconButton(Icons.CLOSE_OUTLINED, on_click=page.pop_dialog, tooltip=Tooltip("Закрыть окно", vertical_offset=15),
                icon_color=self.__COLORS["default"])])
            )

    def Launch(self) -> None:
        if self.__data_manager.UnpackData():
            self.__data_gainer.UpdateSettings()
        self.__data_manager.InsertData("active", self.__zapret_launcher.CheckIfZapretIsRunning())
        update_available: bool = self.__data_gainer.CheckForUpdates() 
        run(lambda page: self.__Body(page, update_available))