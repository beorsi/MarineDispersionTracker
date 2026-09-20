import flet as flet
from Data.species import SPECIES
from Data.dataProcess import getSpeciesStats

CARD_WIDTH = 480

COLOR_BG = "#152E45"
COLOR_ACCENT = "#1A7FA8"
COLOR_SURFACE = "#1C3D57"
COLOR_TEXT = "#E8F4F8"
COLOR_MUTED = "#7BAFC4"
COLOR_DIVIDER = "#1E4D6B"


def _section_label(text: str) -> flet.Text:
    return flet.Text(text, size=11, color=COLOR_ACCENT, font_family="Intel", weight=flet.FontWeight.BOLD)


def _stat_row(label: str, value: str) -> flet.Container:
    return flet.Container(
        padding=flet.Padding(left=14, top=8, right=14, bottom=8),
        bgcolor=COLOR_SURFACE,
        border_radius=8,
        content=flet.Row(
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                flet.Text(label, size=13, color=COLOR_MUTED, font_family="Intel"),
                flet.Text(value, size=13, color=COLOR_TEXT, font_family="Intel", weight=flet.FontWeight.BOLD),
            ],
        ),
    )


def _divider() -> flet.Container:
    return flet.Container(height=1, bgcolor=COLOR_DIVIDER, margin=flet.Margin(left=0, top=16, right=0, bottom=16))


def build_species_card(scientific_name: str, page: flet.Page) -> flet.Container:
    species_data = SPECIES.get(scientific_name)
    common_name = species_data["common_name"] if species_data else "Unknown species"

    loading_indicator = flet.Row(
        alignment=flet.MainAxisAlignment.CENTER,
        controls=[
            flet.ProgressRing(width=18, height=18, stroke_width=2, color=COLOR_ACCENT),
            flet.Text("  Loading occurrence data...", size=13, color=COLOR_MUTED, font_family="Intel"),
        ],
    )
    body = flet.Column(controls=[loading_indicator], spacing=6)

    def load_stats():
        try:
            stats = getSpeciesStats(scientific_name)

            record_types = stats["record_types"]
            record_rows = [_stat_row(rtype if rtype != "Occurrence" else "Unclassified", f"{count:,}") for rtype, count in record_types.items()]

            body.controls = [
                _section_label("OCCURRENCE DATA"),
                flet.Container(height=6),
                _stat_row("Total records (OBIS)", f"{stats['total']:,}"),
                _stat_row("Records fetched", f"{sum(record_types.values()):,}"),
                _stat_row("Year range", f"{stats['first_occurrence']} – {stats['last_occurrence']}" if stats['first_occurrence'] else "N/A"),
                _stat_row("Last occurrence", str(stats['last_occurrence']) if stats['last_occurrence'] else "N/A"),

                _divider(),
                _section_label("HABITAT"),
                flet.Container(height=6),
                _stat_row("Average depth", f"{stats['avg_depth_m']} m" if stats['avg_depth_m'] is not None else "N/A"),
                _stat_row("Average shore distance", f"{stats['avg_shore_km']} km" if stats['avg_shore_km'] is not None else "N/A"),
                _stat_row("Most common locality", stats['top_locality'] if stats['top_locality'] else "N/A"),

                _divider(),
                _section_label("RECORD TYPES"),
                flet.Container(height=6),
                *record_rows,
            ]
        except Exception as e:
            body.controls = [
                flet.Text(f"Failed to load data: {e}", size=13, color="#E05C5C", font_family="Intel")
            ]
        finally:
            page.update()

    card = flet.Container(
        width=CARD_WIDTH,
        expand=True,
        bgcolor=COLOR_BG,
        border_radius=16,
        padding=24,
        opacity=1,
        animate_opacity=flet.Animation(400, flet.AnimationCurve.EASE_IN),
        content=flet.Column(
            spacing=0,
            scroll=flet.ScrollMode.AUTO,
            controls=[
                flet.Text(common_name, size=26, weight=flet.FontWeight.BOLD, color=COLOR_TEXT, font_family="Intel"),
                flet.Text(scientific_name, size=14, italic=True, color=COLOR_MUTED, font_family="Intel"),
                _divider(),
                body,
            ],
        ),
    )

    def load_stats_and_fade():
        load_stats()
        card.opacity = 1
        page.update()

    page.run_thread(load_stats_and_fade)

    return card
