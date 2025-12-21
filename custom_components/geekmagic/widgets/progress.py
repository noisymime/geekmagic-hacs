"""Progress widget for GeekMagic displays."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from ..const import COLOR_CYAN, COLOR_DARK_GRAY, COLOR_GRAY, COLOR_WHITE
from .base import Widget, WidgetConfig
from .components import Bar, Color, Column, Component, Icon, Row, Spacer, Text
from .helpers import format_number

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import EntityState, WidgetState


def _extract_numeric(entity: EntityState | None) -> float:
    """Extract numeric value from entity state."""
    if entity is None:
        return 0.0
    try:
        return float(entity.state)
    except (ValueError, TypeError):
        return 0.0


@dataclass
class ProgressDisplay(Component):
    """Progress bar display component."""

    value: float
    target: float = 100
    label: str = "Progress"
    unit: str = ""
    color: Color = COLOR_CYAN
    icon: str | None = None
    show_target: bool = True
    bar_height_style: str = "normal"

    BAR_HEIGHT_MULTIPLIERS: ClassVar[dict[str, float]] = {
        "thin": 0.10,
        "normal": 0.17,
        "thick": 0.25,
    }

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render progress display."""
        padding = int(width * 0.05)
        icon_size = max(10, int(height * 0.20))
        bar_height_mult = self.BAR_HEIGHT_MULTIPLIERS.get(self.bar_height_style, 0.17)
        bar_height = max(4, int(height * bar_height_mult))

        # Format numbers with abbreviations for large values
        display_value = format_number(self.value)
        target = self.target or 100
        display_target = format_number(target)
        percent = min(100, (self.value / target) * 100) if target > 0 else 0

        # Adaptive layout based on size
        is_compact = height < 100

        if is_compact:
            # Compact: icon + value on first line, bar + percent on second
            value_text = f"{display_value}/{display_target}" if self.show_target else display_value
            if self.unit:
                value_text += f" {self.unit}"

            # Row 1: Icon + Value
            row1_children = []
            if self.icon:
                row1_children.append(Icon(name=self.icon, size=icon_size, color=self.color))
            row1_children.append(
                Text(text=value_text, font="small", color=COLOR_WHITE, align="start")
            )

            # Row 2: Progress bar + percent
            row2_children = [
                Bar(
                    percent=percent,
                    color=self.color,
                    background=COLOR_DARK_GRAY,
                    height=bar_height,
                ),
                Text(text=f"{percent:.0f}%", font="tiny", color=COLOR_WHITE, align="end"),
            ]

            # Build column with two rows
            Column(
                children=[
                    Row(children=row1_children, gap=4, align="center", padding=padding),
                    Row(children=row2_children, gap=8, align="center", padding=padding),
                ],
                gap=int(height * 0.10),
                justify="center",
            ).render(ctx, x, y, width, height)

        else:
            # Full layout: label + value on first line, bar + percent on second
            value_text = f"{display_value}/{display_target}" if self.show_target else display_value
            if self.unit:
                value_text += f" {self.unit}"

            # Top row: Icon + Label + Spacer + Value
            top_row_children = []
            if self.icon:
                top_row_children.append(Icon(name=self.icon, size=icon_size, color=self.color))

            # Check if label fits by measuring
            font_label = ctx.get_font("small")
            font_value = ctx.get_font("regular")
            label_text = self.label.upper()
            label_width, _ = ctx.get_text_size(label_text, font_label)
            value_width, _ = ctx.get_text_size(value_text, font_value)
            icon_width = icon_size + 4 if self.icon else 0
            available_for_label = width - padding * 2 - icon_width - value_width - 8

            if available_for_label >= label_width:
                # Label fits - add label, spacer, value
                top_row_children.extend(
                    [
                        Text(text=label_text, font="small", color=COLOR_GRAY, align="start"),
                        Spacer(),
                        Text(text=value_text, font="regular", color=COLOR_WHITE, align="end"),
                    ]
                )
            else:
                # Not enough space - value only
                top_row_children.append(
                    Text(text=value_text, font="regular", color=COLOR_WHITE, align="start")
                )

            # Bottom row: Bar + Percent
            bottom_row_children = [
                Bar(
                    percent=percent,
                    color=self.color,
                    background=COLOR_DARK_GRAY,
                    height=bar_height,
                ),
                Text(text=f"{percent:.0f}%", font="small", color=COLOR_WHITE, align="end"),
            ]

            # Build column with two rows
            Column(
                children=[
                    Row(children=top_row_children, gap=4, align="center", padding=padding),
                    Row(children=bottom_row_children, gap=8, align="center", padding=padding),
                ],
                gap=int(height * 0.10),
                justify="center",
            ).render(ctx, x, y, width, height)


class ProgressWidget(Widget):
    """Widget that displays progress with label."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the progress widget."""
        super().__init__(config)
        self.target = config.options.get("target", 100)
        self.unit = config.options.get("unit", "")
        self.show_target = config.options.get("show_target", True)
        self.icon = config.options.get("icon")
        self.bar_height_style = config.options.get("bar_height", "normal")

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the progress widget."""
        entity = state.entity
        value = _extract_numeric(entity)

        unit = self.unit
        if not unit and entity:
            unit = entity.unit or ""

        label = self.config.label
        if not label and entity:
            label = entity.friendly_name
        label = label or "Progress"

        return ProgressDisplay(
            value=value,
            target=self.target,
            label=label,
            unit=unit,
            color=self.config.color or COLOR_CYAN,
            icon=self.icon,
            show_target=self.show_target,
            bar_height_style=self.bar_height_style,
        )


@dataclass
class MultiProgressDisplay(Component):
    """Multi-progress list display component."""

    items: list[dict] = field(default_factory=list)
    title: str | None = None

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render multi-progress list."""
        padding = int(width * 0.05)
        row_count = len(self.items) or 1

        # Calculate sizes
        title_height = int(height * 0.14) if self.title else 0
        available_height = height - title_height - padding * 2
        row_height = min(int(height * 0.35), available_height // row_count)
        bar_height = max(4, int(height * 0.06))
        icon_size = max(8, int(height * 0.09))

        # Build component tree
        children = []

        # Add title if present
        if self.title:
            children.append(
                Row(
                    children=[
                        Text(text=self.title.upper(), font="small", color=COLOR_GRAY, align="start")
                    ],
                    padding=padding,
                )
            )

        # Build each progress item row
        for item in self.items:
            label = item.get("label", "Item")
            value = item.get("value", 0)
            target = item.get("target", 100)
            color = item.get("color", COLOR_CYAN)
            icon = item.get("icon")
            unit = item.get("unit", "")

            percent = min(100, (value / target) * 100) if target > 0 else 0
            value_text = f"{value:.0f}/{target:.0f}"
            if unit:
                value_text += f" {unit}"

            # Top row: Icon + Label + Spacer + Value
            top_row_children = []
            if icon:
                top_row_children.append(Icon(name=icon, size=icon_size, color=color))
            top_row_children.extend(
                [
                    Text(text=label.upper(), font="tiny", color=COLOR_GRAY, align="start"),
                    Spacer(),
                    Text(text=value_text, font="tiny", color=COLOR_WHITE, align="end"),
                ]
            )

            # Bottom row: Bar + Percent
            bottom_row_children = [
                Bar(percent=percent, color=color, background=COLOR_DARK_GRAY, height=bar_height),
                Text(text=f"{percent:.0f}%", font="tiny", color=COLOR_WHITE, align="end"),
            ]

            # Combine into a column for this item
            item_column = Column(
                children=[
                    Row(children=top_row_children, gap=4, align="center", padding=padding),
                    Row(children=bottom_row_children, gap=8, align="center", padding=padding),
                ],
                gap=int(row_height * 0.15),
                justify="center",
            )
            children.append(item_column)

        # Render the entire column
        Column(
            children=children,
            gap=int(height * 0.02),
            justify="start",
            padding=0,
        ).render(ctx, x, y, width, height)


class MultiProgressWidget(Widget):
    """Widget that displays multiple progress items."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the multi-progress widget."""
        super().__init__(config)
        self.items = config.options.get("items", [])
        self.title = config.options.get("title")

    def get_entities(self) -> list[str]:
        """Return list of entity IDs."""
        return [item.get("entity_id") for item in self.items if item.get("entity_id")]

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the multi-progress widget."""
        display_items = []
        for item in self.items:
            entity_id = item.get("entity_id")
            entity = state.get_entity(entity_id) if entity_id else None
            value = _extract_numeric(entity)

            label = item.get("label", "")
            if entity and not label:
                label = entity.friendly_name
            label = label or entity_id or "Item"

            unit = item.get("unit", "")
            if entity and not unit:
                unit = entity.unit or ""

            display_items.append(
                {
                    "label": label,
                    "value": value,
                    "target": item.get("target", 100),
                    "color": item.get("color", COLOR_CYAN),
                    "icon": item.get("icon"),
                    "unit": unit,
                }
            )

        return MultiProgressDisplay(items=display_items, title=self.title)
