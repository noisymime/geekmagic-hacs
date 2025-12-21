"""Entity widget for GeekMagic displays."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import (
    COLOR_CYAN,
    COLOR_GRAY,
    COLOR_WHITE,
    PLACEHOLDER_NAME,
    PLACEHOLDER_VALUE,
)
from .base import Widget, WidgetConfig
from .component_helpers import CenteredValue, IconValue
from .components import Component, Panel
from .helpers import (
    estimate_max_chars,
    format_value_with_unit,
    truncate_text,
)

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import WidgetState


def _get_entity_icon(entity_state) -> str | None:
    """Get icon from entity state, handling MDI format."""
    if entity_state is None:
        return None
    icon = entity_state.icon
    if icon and icon.startswith("mdi:"):
        return icon[4:]  # Strip "mdi:" prefix
    return None


def _get_unit(entity_state) -> str:
    """Get unit of measurement from entity state."""
    if entity_state is None:
        return ""
    return entity_state.unit or ""


def _resolve_label(config, entity_state, default: str = "") -> str:
    """Get label from config or entity friendly_name."""
    if config.label:
        return config.label
    if entity_state:
        return entity_state.friendly_name
    return default


class EntityWidget(Widget):
    """Widget that displays a Home Assistant entity state."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the entity widget."""
        super().__init__(config)
        self.show_name = config.options.get("show_name", True)
        self.show_unit = config.options.get("show_unit", True)
        self.show_icon = config.options.get("show_icon", True)
        self.icon = config.options.get("icon")  # Explicit icon override
        self.show_panel = config.options.get("show_panel", False)
        self.precision = config.options.get("precision")  # Decimal places for numeric values

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the entity widget.

        Args:
            ctx: RenderContext for drawing
            state: Widget state with entity data

        Returns:
            Component tree for rendering
        """
        entity = state.entity

        if entity is None:
            value = PLACEHOLDER_VALUE
            unit = ""
            name = self.config.label or self.config.entity_id or PLACEHOLDER_NAME
        else:
            value = entity.state
            # Apply precision formatting if specified and value is numeric
            if self.precision is not None:
                try:
                    numeric_value = float(value)
                    value = f"{numeric_value:.{self.precision}f}"
                except (ValueError, TypeError):
                    pass  # Keep original value if not numeric
            unit = _get_unit(entity) if self.show_unit else ""
            name = _resolve_label(self.config, entity, entity.entity_id)

        # Truncate value and name
        max_value_chars = estimate_max_chars(ctx.width, char_width=6, padding=6)
        max_name_chars = estimate_max_chars(ctx.width, char_width=5, padding=4)
        value = truncate_text(value, max_value_chars, style="middle")
        name = truncate_text(name, max_name_chars, style="middle")

        color = self.config.color or COLOR_CYAN
        value_text = format_value_with_unit(value, unit)
        label = name if self.show_name else None

        # Determine icon to use
        icon = self.icon
        if not icon and self.show_icon:
            icon = _get_entity_icon(entity)

        # Build component based on whether we have an icon
        if icon:
            content = IconValue(
                icon=icon,
                value=value_text,
                label=label or "",
                color=color,
                value_color=COLOR_WHITE,
                label_color=COLOR_GRAY,
            )
        else:
            content = CenteredValue(
                value=value_text,
                label=label,
                value_color=color,
                label_color=COLOR_GRAY,
            )

        # Wrap in panel if enabled
        if self.show_panel:
            return Panel(child=content)

        return content
