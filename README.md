# GeekMagic Display for Home Assistant

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

A Home Assistant custom integration for GeekMagic displays (SmallTV Pro and similar ESP8266-based devices).

## Dashboard Samples

<p align="center">
  <img src="samples/01_system_monitor.png" alt="System Monitor" width="120">
  <img src="samples/02_smart_home.png" alt="Smart Home" width="120">
  <img src="samples/03_weather.png" alt="Weather" width="120">
  <img src="samples/04_server_stats.png" alt="Server Stats" width="120">
</p>

<p align="center">
  <img src="samples/05_media_player.png" alt="Media Player" width="120">
  <img src="samples/06_energy_monitor.png" alt="Energy Monitor" width="120">
  <img src="samples/07_fitness.png" alt="Fitness Tracker" width="120">
  <img src="samples/08_clock_dashboard.png" alt="Clock Dashboard" width="120">
</p>

<p align="center">
  <img src="samples/09_network_monitor.png" alt="Network Monitor" width="120">
  <img src="samples/10_thermostat.png" alt="Thermostat" width="120">
  <img src="samples/11_batteries.png" alt="Batteries" width="120">
  <img src="samples/12_security.png" alt="Security" width="120">
</p>

## Features

- **12 widget types**: Clock, entity, media, chart, text, gauge, progress, weather, status, camera, and more
- **5 layout options**: Grid (2x2, 2x3), hero, split, three-column
- **Entity-based configuration**: Configure via Home Assistant entities (WLED-style)
- **Multi-screen support**: Up to 10 screens with auto-cycling
- **Pure Python rendering**: Uses Pillow for image generation (no browser required)
- **Configurable refresh**: Updates every 5-300 seconds

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click "Custom repositories"
3. Add this repository URL
4. Install "GeekMagic Display"
5. Restart Home Assistant

### Manual

1. Copy `custom_components/geekmagic` to your Home Assistant's `custom_components` folder
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "GeekMagic"
4. Enter your device's IP address

### Initial Setup

After adding the integration, your device will display a welcome screen with live data until you configure a dashboard:

<p align="center">
  <img src="samples/00_welcome_screen.png" alt="Welcome Screen" width="180">
</p>

The welcome screen shows:
- **Current time and date** - Updates every refresh interval
- **Home Assistant version** - Your HA instance version
- **Entity count** - Total entities in your system
- **Configure hint** - Reminder to set up your dashboard

---

## Entity-Based Configuration (WLED-Style)

GeekMagic uses **entity-based configuration** similar to WLED. Instead of navigating through settings menus, you configure your display directly through Home Assistant entities on the device page.

### Device Entities

After setup, your device exposes these configuration entities:

#### Device Controls
| Entity | Type | Description |
|--------|------|-------------|
| `number.xxx_brightness` | Number | Display brightness (0-100) |
| `number.xxx_refresh_interval` | Number | Update interval in seconds (5-300) |
| `number.xxx_screen_cycle_interval` | Number | Auto-cycle screens (0=disabled, 5-300s) |
| `number.xxx_screen_count` | Number | Number of screens (1-10) |
| `select.xxx_current_screen` | Select | Active screen selector |

#### Action Buttons
| Entity | Type | Description |
|--------|------|-------------|
| `button.xxx_refresh_now` | Button | Force immediate display update |
| `button.xxx_next_screen` | Button | Switch to next screen |
| `button.xxx_previous_screen` | Button | Switch to previous screen |

#### Diagnostic Sensors
| Entity | Type | Description |
|--------|------|-------------|
| `sensor.xxx_status` | Sensor | Connection status (connected/disconnected) |
| `sensor.xxx_current_screen_name` | Sensor | Name of the currently active screen |

### Per-Screen Entities

Each screen has its own configuration entities:

| Entity | Type | Description |
|--------|------|-------------|
| `text.xxx_screen_N_name` | Text | Screen name |
| `select.xxx_screen_N_layout` | Select | Layout type (grid, hero, split, etc.) |

### Per-Slot Entities

Each slot in a layout has widget configuration:

| Entity | Type | Description |
|--------|------|-------------|
| `select.xxx_screen_N_slot_M_widget` | Select | Widget type |
| `text.xxx_screen_N_slot_M_entity` | Text | Home Assistant entity ID to display |
| `text.xxx_screen_N_slot_M_label` | Text | Custom label (optional) |

### Widget Option Switches

Boolean options for each widget type appear as switches:

| Widget | Options |
|--------|---------|
| Clock | `show_seconds`, `show_date` |
| Entity | `show_name`, `show_unit`, `show_panel` |
| Chart | `show_value`, `show_range` |
| Media | `show_artist`, `show_album`, `show_progress` |
| Weather | `show_forecast`, `show_humidity`, `show_wind` |
| Progress | `show_target` |
| Camera | `show_label` |

---

## Configuration Examples

### Weather Dashboard (Hero Layout)

A weather-focused display with forecast and indoor conditions.

```yaml
# Screen: Hero layout (4 slots)
# Slot 0 (hero): Weather widget with forecast
# Slot 1-3 (footer): Indoor temp, humidity, outdoor temp

# Configure via entities:
select.geekmagic_display_screen_1_layout: "Hero (4 slots)"
select.geekmagic_display_screen_1_slot_1_widget: "Weather"
text.geekmagic_display_screen_1_slot_1_entity: "weather.home"
select.geekmagic_display_screen_1_slot_2_widget: "Entity"
text.geekmagic_display_screen_1_slot_2_entity: "sensor.living_room_temperature"
select.geekmagic_display_screen_1_slot_3_widget: "Entity"
text.geekmagic_display_screen_1_slot_3_entity: "sensor.living_room_humidity"
select.geekmagic_display_screen_1_slot_4_widget: "Entity"
text.geekmagic_display_screen_1_slot_4_entity: "sensor.outdoor_temperature"
```

### System Monitor (Grid 2x2)

Monitor your server or Home Assistant host.

```yaml
# Screen: Grid 2x2 layout (4 slots)
# 4 gauge widgets showing CPU, Memory, Disk, Network

select.geekmagic_display_screen_1_layout: "Grid 2x2 (4 slots)"
select.geekmagic_display_screen_1_slot_1_widget: "Gauge"
text.geekmagic_display_screen_1_slot_1_entity: "sensor.processor_use"
select.geekmagic_display_screen_1_slot_2_widget: "Gauge"
text.geekmagic_display_screen_1_slot_2_entity: "sensor.memory_use_percent"
select.geekmagic_display_screen_1_slot_3_widget: "Gauge"
text.geekmagic_display_screen_1_slot_3_entity: "sensor.disk_use_percent"
select.geekmagic_display_screen_1_slot_4_widget: "Chart"
text.geekmagic_display_screen_1_slot_4_entity: "sensor.network_throughput_in"
```

### Media Player (Hero Layout)

Display now playing with album art.

```yaml
# Screen: Hero layout
# Slot 0 (hero): Media player with album art
# Slot 1-3: Additional info

select.geekmagic_display_screen_1_layout: "Hero (4 slots)"
select.geekmagic_display_screen_1_slot_1_widget: "Media Player"
text.geekmagic_display_screen_1_slot_1_entity: "media_player.spotify"
select.geekmagic_display_screen_1_slot_2_widget: "Text"
select.geekmagic_display_screen_1_slot_3_widget: "Entity"
text.geekmagic_display_screen_1_slot_3_entity: "sensor.living_room_temperature"
select.geekmagic_display_screen_1_slot_4_widget: "Clock"
```

### Smart Home Overview (Grid 2x3)

6 entity slots for a compact home status view.

```yaml
# Screen: Grid 2x3 layout (6 slots)
# Mix of temperature, humidity, and status widgets

select.geekmagic_display_screen_1_layout: "Grid 2x3 (6 slots)"
select.geekmagic_display_screen_1_slot_1_widget: "Entity"
text.geekmagic_display_screen_1_slot_1_entity: "sensor.living_room_temperature"
select.geekmagic_display_screen_1_slot_2_widget: "Entity"
text.geekmagic_display_screen_1_slot_2_entity: "sensor.living_room_humidity"
select.geekmagic_display_screen_1_slot_3_widget: "Status"
text.geekmagic_display_screen_1_slot_3_entity: "binary_sensor.front_door"
select.geekmagic_display_screen_1_slot_4_widget: "Status"
text.geekmagic_display_screen_1_slot_4_entity: "binary_sensor.motion_sensor"
select.geekmagic_display_screen_1_slot_5_widget: "Entity"
text.geekmagic_display_screen_1_slot_5_entity: "light.living_room"
select.geekmagic_display_screen_1_slot_6_widget: "Status"
text.geekmagic_display_screen_1_slot_6_entity: "person.john"
```

### Clock & Temperature (Split Layout)

Large clock with chart on the side.

```yaml
# Screen: Split layout (2 slots)
# Slot 0: Large clock
# Slot 1: Temperature chart

select.geekmagic_display_screen_1_layout: "Split (2 slots)"
select.geekmagic_display_screen_1_slot_1_widget: "Clock"
select.geekmagic_display_screen_1_slot_2_widget: "Chart"
text.geekmagic_display_screen_1_slot_2_entity: "sensor.outdoor_temperature"
```

### Example Automations

```yaml
# Cycle screens based on time of day
automation:
  - alias: "Morning dashboard"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: select.select_option
        target:
          entity_id: select.geekmagic_display_current_screen
        data:
          option: "Weather"

  - alias: "Evening dashboard"
    trigger:
      - platform: time
        at: "18:00:00"
    action:
      - service: select.select_option
        target:
          entity_id: select.geekmagic_display_current_screen
        data:
          option: "Media"
```

```yaml
# Show security camera when motion detected
automation:
  - alias: "Show camera on motion"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_motion
        to: "on"
    action:
      - service: select.select_option
        target:
          entity_id: select.geekmagic_display_screen_1_slot_1_widget
        data:
          option: "Camera"
      - service: text.set_value
        target:
          entity_id: text.geekmagic_display_screen_1_slot_1_entity
        data:
          value: "camera.front_door"
```

---

## Widgets

### Widget Gallery

Widgets automatically adapt their layout based on cell size:

| Widget | 1x1 | 1x2 | 2x1 | 2x2 | 2x3 | 3x3 |
|--------|-----|-----|-----|-----|-----|-----|
| **Gauge (Bar)** | <img src="samples/widgets/gauge_bar_1x1.png" width="60"> | <img src="samples/widgets/gauge_bar_1x2.png" width="60"> | <img src="samples/widgets/gauge_bar_2x1.png" width="60"> | <img src="samples/widgets/gauge_bar_2x2.png" width="60"> | <img src="samples/widgets/gauge_bar_2x3.png" width="60"> | <img src="samples/widgets/gauge_bar_3x3.png" width="60"> |
| **Gauge (Ring)** | <img src="samples/widgets/gauge_ring_1x1.png" width="60"> | <img src="samples/widgets/gauge_ring_1x2.png" width="60"> | <img src="samples/widgets/gauge_ring_2x1.png" width="60"> | <img src="samples/widgets/gauge_ring_2x2.png" width="60"> | <img src="samples/widgets/gauge_ring_2x3.png" width="60"> | <img src="samples/widgets/gauge_ring_3x3.png" width="60"> |
| **Entity (Icon)** | <img src="samples/widgets/entity_icon_1x1.png" width="60"> | <img src="samples/widgets/entity_icon_1x2.png" width="60"> | <img src="samples/widgets/entity_icon_2x1.png" width="60"> | <img src="samples/widgets/entity_icon_2x2.png" width="60"> | <img src="samples/widgets/entity_icon_2x3.png" width="60"> | <img src="samples/widgets/entity_icon_3x3.png" width="60"> |
| **Entity (Plain)** | <img src="samples/widgets/entity_plain_1x1.png" width="60"> | <img src="samples/widgets/entity_plain_1x2.png" width="60"> | <img src="samples/widgets/entity_plain_2x1.png" width="60"> | <img src="samples/widgets/entity_plain_2x2.png" width="60"> | <img src="samples/widgets/entity_plain_2x3.png" width="60"> | <img src="samples/widgets/entity_plain_3x3.png" width="60"> |

### Other Widgets

<p>
<img src="samples/widgets/widget_clock.png" width="100" title="Clock">
<img src="samples/widgets/widget_media.png" width="100" title="Media">
<img src="samples/widgets/widget_chart.png" width="100" title="Chart">
<img src="samples/widgets/widget_text.png" width="100" title="Text">
<img src="samples/widgets/widget_gauge_arc.png" width="100" title="Gauge Arc">
<img src="samples/widgets/widget_progress.png" width="100" title="Progress">
<img src="samples/widgets/widget_multi_progress.png" width="100" title="Multi-Progress">
<img src="samples/widgets/widget_weather.png" width="100" title="Weather">
<img src="samples/widgets/widget_status.png" width="100" title="Status">
<img src="samples/widgets/widget_status_list.png" width="100" title="Status List">
</p>

### Widget Types

| Type | Description |
|------|-------------|
| `camera` | Camera snapshot display |
| `clock` | Time and date |
| `entity` | Any HA entity value (with optional icon) |
| `media` | Now playing from media player |
| `chart` | Sparkline from entity history |
| `text` | Static or dynamic text |
| `gauge` | Bar, ring, or arc gauge (`style: bar/ring/arc`) |
| `progress` | Goal tracking with progress bar |
| `multi_progress` | Multiple progress items |
| `weather` | Weather with forecast |
| `status` | Binary sensor indicator |
| `status_list` | Multiple status indicators |

---

## Layouts

### Available Layout Types

| Layout | Type | Slots | Description |
|--------|------|-------|-------------|
| Grid 2x2 | `grid_2x2` | 4 | 2x2 grid of equal widgets |
| Grid 2x3 | `grid_2x3` | 6 | 2 rows, 3 columns |
| Hero | `hero` | 4 | Large hero + 3 footer widgets |
| Split | `split` | 2 | Left/right or top/bottom panels |
| Three Column | `three_column` | 3 | 3 vertical columns |

### Layout Examples

#### Grid 2x2
<img src="samples/layouts/layout_grid_2x2.png" alt="Grid 2x2" width="180">

4 equal slots in a 2x2 arrangement. Each slot is ~112x112px.

```
+-------+-------+
|   0   |   1   |
+-------+-------+
|   2   |   3   |
+-------+-------+
```

**Best for**: 4 medium widgets (gauges, entities)

#### Grid 2x3
<img src="samples/layouts/layout_grid_2x3.png" alt="Grid 2x3" width="180">

6 slots in 2 rows, 3 columns. Each slot is ~75x112px.

```
+-----+-----+-----+
|  0  |  1  |  2  |
+-----+-----+-----+
|  3  |  4  |  5  |
+-----+-----+-----+
```

**Best for**: 6 entity values, compact dashboard

#### Hero Layout
<img src="samples/layouts/layout_hero.png" alt="Hero Layout" width="180">

Large hero slot (70% height) + 3 footer widgets.

```
+-------------------+
|                   |
|    HERO (0)       |
|                   |
+-----+------+------+
|  1  |   2  |   3  |
+-----+------+------+
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `footer_slots` | int | `3` | Number of footer widgets |
| `hero_ratio` | float | `0.7` | Hero height ratio (0.5-0.8) |

**Best for**: Weather + stats, clock + info, media player

#### Split
<img src="samples/layouts/layout_split_vertical.png" alt="Split Layout" width="180">

Two panels (left/right or top/bottom).

```
Vertical (default):     Horizontal:
+----------+----------+ +---------------------+
|          |          | |         0           |
|    0     |    1     | +---------------------+
|          |          | |         1           |
+----------+----------+ +---------------------+
```

**Best for**: Clock + chart, media + status, large widget pairs

#### Three Column
<img src="samples/layouts/layout_three_column.png" alt="Three Column" width="180">

Three vertical columns with customizable widths.

```
+------+------+------+
|      |      |      |
|  0   |  1   |  2   |
|      |      |      |
+------+------+------+
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ratios` | tuple | `(0.33, 0.34, 0.33)` | Column width ratios |

**Best for**: 3 gauges, 3 status lists, comparison view

---

## Services

| Service | Description |
|---------|-------------|
| `geekmagic.refresh` | Force immediate display update |
| `geekmagic.brightness` | Set display brightness (0-100) |
| `geekmagic.set_screen` | Switch to a specific screen by index |
| `geekmagic.next_screen` | Switch to the next screen |
| `geekmagic.previous_screen` | Switch to the previous screen |

> **Tip**: For most use cases, you can use the entity-based controls instead of services. For example, use the `button.xxx_next_screen` entity or `select.xxx_current_screen` entity for screen navigation.

## Device Compatibility

Tested with:
- GeekMagic SmallTV Pro (240x240, ESP8266)

Should work with any GeekMagic device that supports the `/doUpload` HTTP API.

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint and type check
uv run ruff check .
uv run ty check

# Run all checks (pre-commit)
uv run pre-commit run --all-files

# Generate sample images
uv run python scripts/generate_samples.py
uv run python scripts/generate_widget_samples.py
uv run python scripts/generate_layout_samples.py
```

## License

MIT
