import flet as ft

def get_progress_ring():
    return ft.ProgressRing(
        width=100,
        height=100,
        expand=True
    )