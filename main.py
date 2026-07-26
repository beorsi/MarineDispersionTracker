import flet as flet
import asyncio
from UI.speciesCard import build_species_card
from UI.sidebar import build_sidebar

async def main(page: flet.Page):
    page.window.width = 1920
    page.window.height = 1080
    page.window.resizable = True
    page.window.left = 0
    page.window.top = 0
    page.bgcolor = "#0D2137"
    page.fonts = {
        "Intel": "assets/fonts/IntelOneMono-VariableFont_wght.ttf"
    }
    page.padding = 0

    selected_species = "Physeter macrocephalus"

    sidebar_container = flet.Container(width=300, height=1020)
    card_area = flet.Container(
        width=1620,
        height=1020,
        bgcolor="#0D2137",
        padding=50,
        alignment=flet.Alignment(1, -1),
    )

    def on_select(scientific_name: str):
        nonlocal selected_species
        selected_species = scientific_name
        sidebar_container.content = build_sidebar(selected_species, on_select, page).content
        card_area.content = build_species_card(selected_species, page)
        page.update()

    sidebar_container.content = build_sidebar(selected_species, on_select, page).content

    page.add(
        flet.Column(
            controls=[
                flet.Row(
                    spacing=0,
                    controls=[
                        flet.Container(
                            width=1880,
                            height=60,
                            padding=0,
                            alignment=flet.Alignment(0, 0),
                            content=flet.Text("Marine Dispersion Tracker", font_family="Intel", size=32)
                        )
                    ]
                ),
                flet.Row(
                    spacing=0,
                    controls=[
                        sidebar_container,
                        card_area,
                    ]
                )
            ]
        )
    )

    await asyncio.sleep(0.1)
    card_area.content = build_species_card(selected_species, page)
    page.update()


flet.run(main)
