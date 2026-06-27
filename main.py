import flet as flet


async def main(page: flet.Page):
    page.window.width = 1920
    page.window.height = 1080
    page.window.resizable = True
    page.window.left = 0
    page.window.top = 0
    page.bgcolor = "#0D2137"
    page.fonts= {
      "Intel" : "fonts/IntelOneMono-VariableFont_wght.ttf"
    }
    page.padding = 0
    page.add(
    flet.Column(
        controls=[
            flet.Row(
                controls=[
                    flet.Container(
                        width=1920,
                        height=60,
                        padding = 0,
                        alignment = flet.Alignment.CENTER,
                        content = flet.Text("Marine Dispersion Tracker", font_family = "Intel", size = 32)
                        
                    )
                ]
            ),
            flet.Row(
                controls=[
                    flet.Container(
                        width=100,
                        height=1020,
                        bgcolor=flet.Colors.BLUE
                    ),
                    flet.Container(
                        width=1820,
                        height=1020,
                        bgcolor=flet.Colors.GREEN
                    )
                ]
            )
        ]
    )
)


flet.run(main)
