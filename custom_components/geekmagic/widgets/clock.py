"""Clock widget for GeekMagic displays."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from ..const import COLOR_GRAY, COLOR_WHITE
from .base import Widget, WidgetConfig
from .components import Color, Column, Component, FillText, Row, Text

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import WidgetState


@dataclass
class ClockDisplay(Component):
    """Clock display component with time, date, and optional label.

    Time uses FillText to fill available space, date scales proportionally.
    """

    time_str: str
    date_str: str | None = None
    ampm: str | None = None
    label: str | None = None
    time_color: Color = COLOR_WHITE
    date_color: Color = COLOR_GRAY
    label_color: Color = COLOR_GRAY

    def measure(
        self, ctx: RenderContext, max_width: int, max_height: int
    ) -> tuple[int, int]:
        return (max_width, max_height)

    def render(
        self, ctx: RenderContext, x: int, y: int, width: int, height: int
    ) -> None:
        """Render clock with time filling available space."""
        center_x = x + width // 2

        # Calculate space allocation
        has_date = self.date_str is not None and height > 60
        has_label = self.label is not None and height > 80

        # Time gets primary space
        time_height_ratio = 0.55 if has_date else 0.70
        if has_label:
            time_height_ratio *= 0.85

        # Fit time text
        time_font = ctx.fit_text(
            self.time_str,
            max_width=int(width * 0.90),
            max_height=int(height * time_height_ratio),
            bold=False,
        )
        time_w, time_h = ctx.get_text_size(self.time_str, time_font)

        # Calculate positions
        center_y = y + height // 2

        if has_date and self.date_str:
            date_font = ctx.fit_text(
                self.date_str,
                max_width=int(width * 0.90),
                max_height=int(height * 0.18),
            )
            date_h = ctx.get_text_size(self.date_str, date_font)[1]
            gap = int(height * 0.05)
            total_h = time_h + gap + date_h
            time_y = center_y - total_h // 2 + time_h // 2
            date_y = time_y + time_h // 2 + gap + date_h // 2
        else:
            time_y = center_y
            date_y = 0
            date_font = ctx.get_font("tertiary")

        # Adjust for label
        if has_label:
            offset = int(height * 0.08)
            time_y += offset // 2
            date_y += offset // 2

        # Draw time
        ctx.draw_text(
            self.time_str, (center_x, time_y), time_font, self.time_color, "mm"
        )

        # Draw AM/PM
        if self.ampm:
            ampm_font = ctx.get_font("tertiary")
            ampm_x = center_x + time_w // 2 + 3
            ctx.draw_text(
                self.ampm,
                (ampm_x, time_y - time_h // 3),
                ampm_font,
                COLOR_GRAY,
                "lm",
            )

        # Draw date
        if has_date and self.date_str:
            ctx.draw_text(
                self.date_str, (center_x, date_y), date_font, self.date_color, "mm"
            )

        # Draw label
        if has_label and self.label:
            label_font = ctx.get_font("tertiary")
            label_y = y + int(height * 0.10)
            ctx.draw_text(
                self.label.upper(), (center_x, label_y), label_font, self.label_color, "mm"
            )


class ClockWidget(Widget):
    """Widget that displays current time and date."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the clock widget."""
        super().__init__(config)
        self.show_date = config.options.get("show_date", True)
        self.show_seconds = config.options.get("show_seconds", False)
        self.time_format = config.options.get("time_format", "24h")
        self.timezone = config.options.get("timezone")

    def get_entities(self) -> list[str]:
        """Clock widget doesn't depend on entities."""
        return []

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the clock widget as a Component tree.

        Args:
            ctx: RenderContext for drawing
            state: Widget state with current time
        """
        # Get time from state (coordinator handles timezone)
        now = state.now or datetime.now()

        # Format time
        if self.show_seconds:
            if self.time_format == "12h":
                time_str = now.strftime("%I:%M:%S")
                ampm = now.strftime("%p")
            else:
                time_str = now.strftime("%H:%M:%S")
                ampm = None
        elif self.time_format == "12h":
            time_str = now.strftime("%I:%M")
            ampm = now.strftime("%p")
        else:
            time_str = now.strftime("%H:%M")
            ampm = None

        date_str = now.strftime("%a, %b %d") if self.show_date else None
        color = self.config.color or COLOR_WHITE

        return ClockDisplay(
            time_str=time_str,
            date_str=date_str,
            ampm=ampm,
            label=self.config.label,
            time_color=color,
        )
