"""Text widget for GeekMagic displays."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..const import COLOR_GRAY, COLOR_WHITE
from .base import Widget, WidgetConfig
from .components import Column, Component, Text

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import WidgetState


# Map widget align to component align
ALIGN_MAP: dict[str, Literal["start", "center", "end"]] = {
    "left": "start",
    "center": "center",
    "right": "end",
}


class TextWidget(Widget):
    """Widget that displays static or dynamic text."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the text widget."""
        super().__init__(config)
        self.text = config.options.get("text", "")
        self.size = config.options.get("size", "regular")  # small, regular, large, xlarge
        self.align = config.options.get("align", "center")  # left, center, right
        # Entity ID for dynamic text (from options, takes precedence over widget entity_id)
        self.dynamic_entity_id = config.options.get("entity_id")

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the text widget.

        Args:
            ctx: RenderContext for drawing
            state: Widget state with entity data

        Returns:
            Component tree for rendering
        """
        text = self._get_text(state)
        color = self.config.color or COLOR_WHITE
        align = ALIGN_MAP.get(self.align, "center")

        children: list[Component] = []

        # Add label at top if provided
        if self.config.label:
            children.append(Text(self.config.label.upper(), font="small", color=COLOR_GRAY))

        # Main text
        children.append(Text(text, font=self.size, color=color, align=align))

        return Column(
            children=children,
            align="center",
            justify="center",
            gap=4,
        )

    def _get_text(self, state: WidgetState) -> str:
        """Get the text to display.

        If entity_id is set (from options or widget config), returns the entity state.
        Otherwise returns the configured text.
        """
        # Check for entity in state (from config.entity_id or dynamic_entity_id)
        if state.entity:
            return state.entity.state

        # Check for dynamic entity in additional entities
        if self.dynamic_entity_id:
            entity = state.get_entity(self.dynamic_entity_id)
            if entity:
                return entity.state

        return self.text

    def get_entities(self) -> list[str]:
        """Return entity IDs this widget depends on."""
        entities = []
        if self.config.entity_id:
            entities.append(self.config.entity_id)
        if self.dynamic_entity_id and self.dynamic_entity_id != self.config.entity_id:
            entities.append(self.dynamic_entity_id)
        return entities
