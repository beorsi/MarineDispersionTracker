import flet as flet
import flet_map as map
from Data.dataProcess import occurrencesProcessed
from Data.species import SPECIES

COLOR_BG = "#152E45"
COLOR_SURFACE = "#1C3D57"
COLOR_ACCENT = "#4DB8D4"
COLOR_MUTED = "#7BAFC4"
COLOR_TEXT = "#E8F4F8"
COLOR_RED = "#FF4444"


def build_species_map(scientific_name: str, page: flet.Page) -> flet.Column:
    species_data = SPECIES.get(scientific_name)
    common_name = species_data["common_name"] if species_data else "Unknown species"

    marker_layer = map.MarkerLayer(markers=[])

    flet_map = map.Map(
        expand=True,
        initial_center=map.MapLatitudeLongitude(20, 0),
        initial_zoom=2,
        min_zoom=1,
        layers=[
            map.TileLayer(
                url_template="https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
            ),
            marker_layer,
        ],
    )

    loading_overlay = flet.Container(
        expand=True,
        bgcolor=COLOR_BG,
        alignment=flet.Alignment(0, 0),
        content=flet.Row(
            alignment=flet.MainAxisAlignment.CENTER,
            controls=[
                flet.ProgressRing(width=18, height=18, stroke_width=2, color=COLOR_ACCENT),
                flet.Text("  Loading map...", size=13, color=COLOR_MUTED, font_family="Intel"),
            ],
        ),
    )

    stack = flet.Stack(expand=True, controls=[flet_map, loading_overlay])

    map_container = flet.Container(
        height=320,
        bgcolor=COLOR_BG,
        border_radius=flet.BorderRadius(top_left=16, top_right=16, bottom_left=0, bottom_right=0),
        clip_behavior=flet.ClipBehavior.HARD_EDGE,
        content=stack,
    )

    count_text = flet.Text("—", size=13, color=COLOR_TEXT, font_family="Intel", weight=flet.FontWeight.BOLD)

    legend = flet.Container(
        bgcolor=COLOR_SURFACE,
        border_radius=flet.BorderRadius(top_left=0, top_right=0, bottom_left=16, bottom_right=16),
        padding=flet.Padding(left=16, top=12, right=16, bottom=12),
        content=flet.Row(
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                flet.Row(
                    spacing=8,
                    controls=[
                        flet.Container(width=10, height=10, bgcolor=COLOR_RED, border_radius=5),
                        flet.Text("Occurrences", size=12, color=COLOR_MUTED, font_family="Intel"),
                    ],
                ),
                flet.Column(
                    spacing=2,
                    horizontal_alignment=flet.CrossAxisAlignment.END,
                    controls=[
                        flet.Text(common_name, size=12, color=COLOR_TEXT, font_family="Intel", weight=flet.FontWeight.BOLD),
                        flet.Text(scientific_name, size=11, color=COLOR_MUTED, font_family="Intel", italic=True),
                    ],
                ),
                flet.Column(
                    spacing=2,
                    horizontal_alignment=flet.CrossAxisAlignment.END,
                    controls=[
                        flet.Text("Plotted", size=11, color=COLOR_MUTED, font_family="Intel"),
                        count_text,
                    ],
                ),
            ],
        ),
    )

    def load_map():
        try:
            df, _ = occurrencesProcessed(scientific_name)
            coords_df = df[["decimalLatitude", "decimalLongitude"]].dropna()
            marker_layer.markers = [
                map.Marker(
                    content=flet.Container(
                        width=8,
                        height=8,
                        bgcolor=COLOR_RED,
                        border_radius=4,
                        opacity=0.85,
                    ),
                    coordinates=map.MapLatitudeLongitude(row.decimalLatitude, row.decimalLongitude),
                )
                for row in coords_df.itertuples()
            ]
            count_text.value = f"{len(coords_df):,}"
        except Exception:
            count_text.value = "N/A"
        finally:
            stack.controls = [flet_map]
            page.update()

    page.run_thread(load_map)

    image = flet.Container(
        height=220,
        margin=flet.Margin(left=0, top=24, right=0, bottom=0),
        border_radius=16,
        clip_behavior=flet.ClipBehavior.HARD_EDGE,
        content=flet.Image(
            src=species_data["image"] if species_data else "",
            fit=flet.BoxFit.CONTAIN,
            expand=True,
            height=220,
        ),
    )

    title = flet.Container(
        margin=flet.Margin(left=0, top=0, right=0, bottom=8),
        content=flet.Text("Top 1,000 most recent occurrences", size=12, color=COLOR_MUTED, font_family="Intel"),
    )

    return flet.Column(
        expand=True,
        spacing=0,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[title, map_container, legend, image],
    )
