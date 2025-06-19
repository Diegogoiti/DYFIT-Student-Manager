import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo de Tema Flet"

    # Estado inicial del tema
    page.theme_mode = ft.ThemeMode.DARK  # Puedes cambiarlo a LIGHT

    # Función para cambiar el tema
    def switch_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        # Actualizar el icono del botón
        theme_icon_button.icon = (
            ft.Icons.SUNNY if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.NIGHTLIGHT_ROUND
        )
        page.update()

    # Botón para cambiar el tema
    theme_icon_button = ft.IconButton(
        icon=ft.Icons.SUNNY,  # Icono inicial (sol para modo oscuro)
        on_click=switch_theme,
        tooltip="Cambiar tema",
    )

    # Contenido de la página
    page.add(
        ft.Row(
            [
                ft.Text("¡Hola, mundo!", size=20),
                theme_icon_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
