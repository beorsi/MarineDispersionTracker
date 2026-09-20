import flet as flet
import asyncio
from UI.speciesCard import build_species_card
from UI.sidebar import build_sidebar
from UI.speciesMap import build_species_map
from UI.speciesMap import DESKTOP_BREAKPOINT

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
    desktop_layout = False

    sidebar_container = flet.Container(width=220)
    map_area = flet.Container(expand=True, bgcolor="#0D2137", padding=flet.Padding(left=24, top=24, right=24, bottom=24))
    card_area = flet.Container(width=530, expand=True, bgcolor="#0D2137", padding=flet.Padding(left=0, top=24, right=24, bottom=24))

    def on_select(scientific_name: str):
        nonlocal selected_species
        selected_species = scientific_name
        sidebar_container.content = build_sidebar(selected_species, on_select, page).content
        map_area.content = build_species_map(selected_species, page)
        card_area.content = build_species_card(selected_species, page)
        page.update()

    def on_resize(e):
        nonlocal desktop_layout
        new_desktop_layout = (page.width or 0) >= DESKTOP_BREAKPOINT
        if new_desktop_layout != desktop_layout:
            desktop_layout = new_desktop_layout
            map_area.content = build_species_map(selected_species, page)
            page.update()

    page.on_resize = on_resize

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
    desktop_layout = (page.width or 0) >= DESKTOP_BREAKPOINT
    map_area.content = build_species_map(selected_species, page)
    card_area.content = build_species_card(selected_species, page)
    page.update()


flet.run(main)
