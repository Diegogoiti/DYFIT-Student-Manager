import flet as ft
from core.app import MyApp


def Run(page: ft.Page):
    MyApp(page).main()


if __name__ == "__main__":
    ft.app(target=Run)