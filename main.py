import flet as flet
import asyncio
from UI.speciesCard import build_species_card
from UI.sidebar import build_sidebar
from UI.speciesMap import build_species_map

async def main(page: flet.Page):
    page.window.resizable = True
    page.window.left = 0
    page.window.top = 0
    page.bgcolor = "#0D2137"
    page.fonts = {
        "Intel": "assets/fonts/IntelOneMono-VariableFont_wght.ttf"
    }
    page.padding = 0

    selected_species = "Physeter macrocephalus"

    sidebar_container = flet.Container(width=220)
    map_area = flet.Container(expand=True, bgcolor="#0D2137", padding=flet.Padding(left=24, top=24, right=24, bottom=24), alignment=flet.Alignment(0, 0))
    card_area = flet.Container(width=530, expand=True, bgcolor="#0D2137", padding=flet.Padding(left=0, top=24, right=24, bottom=24))

    def on_select(scientific_name: str):
        nonlocal selected_species
        selected_species = scientific_name
        sidebar_container.content = build_sidebar(selected_species, on_select, page).content
        map_area.content = build_species_map(selected_species, page)
        card_area.content = build_species_card(selected_species, page)
        page.update()

    sidebar_container.content = build_sidebar(selected_species, on_select, page).content

    page.add(
        flet.Column(
            expand=True,
            spacing=0,
            controls=[
                flet.Container(
                    height=60,
                    alignment=flet.Alignment(0, 0),
                    content=flet.Text("Marine Dispersion Tracker", font_family="Intel", size=32)
                ),
                flet.Row(
                    spacing=0,
                    expand=True,
                    controls=[
                        sidebar_container,
                        map_area,
                        card_area,
                    ]
                )
            ]
        )
    )

    await asyncio.sleep(0.1)
    map_area.content = build_species_map(selected_species, page)
    card_area.content = build_species_card(selected_species, page)
    page.update()


flet.run(main)
