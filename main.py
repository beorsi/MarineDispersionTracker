import flet as flet


async def main(page: flet.Page):
    page.window.width = 1920
    page.window.height = 1080
    page.window.resizable = True
    page.window.left = 0
    page.window.top = 0
    page.bgcolor = "#0D2137"
    page.add(
      flet.Container(
        height=540,
        width=960,
        bgcolor = flet.Colors.RED
      )
    )


flet.run(main)
