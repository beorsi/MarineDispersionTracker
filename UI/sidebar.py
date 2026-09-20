import flet as flet
from Data.species import SPECIES

COLOR_BG = "#194069"
COLOR_SELECTED_BG = "#0F2D45"
COLOR_ACCENT = "#4DB8D4"
COLOR_TEXT = "#E8F4F8"
COLOR_MUTED = "#7BAFC4"
COLOR_HOVER = "#1A4A75"


def build_sidebar(selected: str, on_select, page: flet.Page) -> flet.Container:

    def make_item(scientific_name: str, common_name: str) -> flet.Container:
        is_selected = scientific_name == selected

        bar = flet.Container(
            width=4,
            height=48,
            bgcolor=COLOR_ACCENT if is_selected else "transparent",
            border_radius=flet.BorderRadius(top_left=0, top_right=2, bottom_left=0, bottom_right=2),
        )

        label = flet.Column(
            spacing=2,
            controls=[
                flet.Text(
                    common_name,
                    size=14,
                    color=COLOR_TEXT,
                    font_family="Intel",
                    weight=flet.FontWeight.BOLD if is_selected else flet.FontWeight.NORMAL,
                ),
                flet.Text(
                    scientific_name,
                    size=11,
                    color=COLOR_ACCENT if is_selected else COLOR_MUTED,
                    font_family="Intel",
                    italic=True,
                ),
            ],
        )

        def on_click(e, sn=scientific_name):
            on_select(sn)

        return flet.Container(
            height=56,
            bgcolor=COLOR_SELECTED_BG if is_selected else "transparent",
            border_radius=8,
            on_click=on_click,
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", COLOR_HOVER if e.data == "true" and not is_selected else (COLOR_SELECTED_BG if is_selected else "transparent")),
                page.update()
            ),
            content=flet.Row(
                spacing=0,
                controls=[
                    bar,
                    flet.Container(width=12),
                    label,
                ],
            ),
        )

    items = [make_item(sn, data["common_name"]) for sn, data in SPECIES.items()]

    return flet.Container(
        width=220,
        bgcolor=COLOR_BG,
        padding=flet.Padding(left=0, top=20, right=12, bottom=20),
        content=flet.Column(
            spacing=4,
            controls=[
                flet.Container(
                    padding=flet.Padding(left=16, top=0, right=0, bottom=12),
                    content=flet.Text("SPECIES", size=11, color=COLOR_MUTED, font_family="Intel", weight=flet.FontWeight.BOLD),
                ),
                *items,
            ],
        ),
    )
