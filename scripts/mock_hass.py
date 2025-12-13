"""Mock Home Assistant for sample generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockState:
    """Mock entity state."""

    entity_id: str
    state: str
    attributes: dict[str, Any] = field(default_factory=dict)


class MockStates:
    """Mock states registry."""

    def __init__(self) -> None:
        """Initialize the mock states registry."""
        self._states: dict[str, MockState] = {}

    def set(self, entity_id: str, state: str, attributes: dict[str, Any] | None = None) -> None:
        """Set a mock entity state."""
        self._states[entity_id] = MockState(
            entity_id=entity_id,
            state=state,
            attributes=attributes or {},
        )

    def get(self, entity_id: str) -> MockState | None:
        """Get a mock entity state."""
        return self._states.get(entity_id)


class MockConfig:
    """Mock Home Assistant config."""

    time_zone_obj = None


class MockHass:
    """Mock Home Assistant instance for sample generation."""

    def __init__(self) -> None:
        """Initialize the mock Home Assistant."""
        self.states = MockStates()
        self.config = MockConfig()


def create_system_monitor_states(hass: MockHass) -> None:
    """Create mock states for system monitor dashboard."""
    hass.states.set("sensor.cpu_usage", "42", {"unit_of_measurement": "%", "friendly_name": "CPU"})
    hass.states.set(
        "sensor.memory_usage", "68", {"unit_of_measurement": "%", "friendly_name": "Memory"}
    )
    hass.states.set(
        "sensor.disk_usage", "65", {"unit_of_measurement": "%", "friendly_name": "Disk"}
    )
    hass.states.set(
        "sensor.network_throughput",
        "48",
        {"unit_of_measurement": "Mb/s", "friendly_name": "Network"},
    )


def create_smart_home_states(hass: MockHass) -> None:
    """Create mock states for smart home dashboard."""
    hass.states.set("light.living_room", "on", {"friendly_name": "Living Room"})
    hass.states.set("light.kitchen", "off", {"friendly_name": "Kitchen"})
    hass.states.set("climate.thermostat", "heat", {"temperature": 22, "friendly_name": "AC"})
    hass.states.set(
        "sensor.temperature", "23.5", {"unit_of_measurement": "°C", "friendly_name": "Temperature"}
    )
    hass.states.set(
        "sensor.humidity", "58", {"unit_of_measurement": "%", "friendly_name": "Humidity"}
    )
    hass.states.set("lock.front_door", "locked", {"friendly_name": "Front Door"})


def create_weather_states(hass: MockHass) -> None:
    """Create mock states for weather dashboard."""
    hass.states.set(
        "weather.home",
        "sunny",
        {
            "temperature": 24,
            "humidity": 45,
            "wind_speed": 12,
            "friendly_name": "Home",
            "forecast": [
                {"datetime": "Mon", "condition": "sunny", "temperature": 26},
                {"datetime": "Tue", "condition": "partlycloudy", "temperature": 23},
                {"datetime": "Wed", "condition": "rainy", "temperature": 19},
            ],
        },
    )


def create_server_stats_states(hass: MockHass) -> None:
    """Create mock states for server stats dashboard."""
    hass.states.set("sensor.server_cpu", "73", {"unit_of_measurement": "%", "friendly_name": "CPU"})
    hass.states.set(
        "sensor.server_memory", "68", {"unit_of_measurement": "%", "friendly_name": "Memory"}
    )
    hass.states.set(
        "sensor.server_disk", "45", {"unit_of_measurement": "%", "friendly_name": "Disk"}
    )
    hass.states.set(
        "sensor.server_load", "2.4", {"unit_of_measurement": "", "friendly_name": "Load"}
    )
    hass.states.set(
        "sensor.server_temp", "58", {"unit_of_measurement": "°C", "friendly_name": "Temp"}
    )
    hass.states.set(
        "sensor.server_uptime", "14d", {"unit_of_measurement": "", "friendly_name": "Uptime"}
    )
    hass.states.set(
        "sensor.server_upload", "125", {"unit_of_measurement": "MB/s", "friendly_name": "Upload"}
    )
    hass.states.set(
        "sensor.server_download", "48", {"unit_of_measurement": "MB/s", "friendly_name": "Download"}
    )


def create_media_player_states(hass: MockHass) -> None:
    """Create mock states for media player dashboard."""
    hass.states.set(
        "media_player.living_room",
        "playing",
        {
            "friendly_name": "Living Room",
            "media_title": "Bohemian Rhapsody",
            "media_artist": "Queen",
            "media_album_name": "A Night at the Opera",
            "media_position": 145,
            "media_duration": 354,
        },
    )


def create_energy_states(hass: MockHass) -> None:
    """Create mock states for energy dashboard."""
    hass.states.set(
        "sensor.energy_consumption",
        "2.4",
        {"unit_of_measurement": "kW", "friendly_name": "Consumption"},
    )
    hass.states.set(
        "sensor.solar_production", "3.2", {"unit_of_measurement": "kW", "friendly_name": "Solar"}
    )
    hass.states.set(
        "sensor.grid_export", "0.8", {"unit_of_measurement": "kW", "friendly_name": "Grid Export"}
    )
    hass.states.set(
        "sensor.energy_today", "18.5", {"unit_of_measurement": "kWh", "friendly_name": "Today"}
    )


def create_fitness_states(hass: MockHass) -> None:
    """Create mock states for fitness dashboard."""
    hass.states.set(
        "sensor.move_calories", "680", {"unit_of_measurement": "cal", "friendly_name": "Move"}
    )
    hass.states.set(
        "sensor.exercise_minutes", "24", {"unit_of_measurement": "min", "friendly_name": "Exercise"}
    )
    hass.states.set(
        "sensor.stand_hours", "12", {"unit_of_measurement": "hr", "friendly_name": "Stand"}
    )
    hass.states.set(
        "sensor.steps", "8542", {"unit_of_measurement": "steps", "friendly_name": "Steps"}
    )
    hass.states.set(
        "sensor.heart_rate", "72", {"unit_of_measurement": "bpm", "friendly_name": "Heart Rate"}
    )
    hass.states.set(
        "sensor.distance", "5.2", {"unit_of_measurement": "km", "friendly_name": "Distance"}
    )


def create_clock_states(hass: MockHass) -> None:
    """Create mock states for clock dashboard."""
    hass.states.set(
        "sensor.outdoor_temp", "18", {"unit_of_measurement": "°C", "friendly_name": "Outside"}
    )
    hass.states.set(
        "calendar.personal",
        "Team Meeting",
        {"friendly_name": "Calendar", "start_time": "10:00 AM"},
    )


def create_network_states(hass: MockHass) -> None:
    """Create mock states for network dashboard."""
    hass.states.set("device_tracker.phone", "home", {"friendly_name": "Phone"})
    hass.states.set("device_tracker.laptop", "home", {"friendly_name": "Laptop"})
    hass.states.set("device_tracker.tablet", "not_home", {"friendly_name": "Tablet"})
    hass.states.set("device_tracker.tv", "home", {"friendly_name": "Smart TV"})
    hass.states.set(
        "sensor.router_download", "85", {"unit_of_measurement": "Mb/s", "friendly_name": "Download"}
    )
    hass.states.set(
        "sensor.router_upload", "42", {"unit_of_measurement": "Mb/s", "friendly_name": "Upload"}
    )
    hass.states.set("sensor.devices_online", "12", {"friendly_name": "Devices Online"})


def create_thermostat_states(hass: MockHass) -> None:
    """Create mock states for thermostat dashboard."""
    hass.states.set(
        "climate.main",
        "heat",
        {
            "temperature": 22,
            "current_temperature": 21.5,
            "humidity": 58,
            "hvac_action": "heating",
            "friendly_name": "Thermostat",
        },
    )
    hass.states.set(
        "sensor.living_temp", "22", {"unit_of_measurement": "°C", "friendly_name": "Living"}
    )
    hass.states.set(
        "sensor.bedroom_temp", "19", {"unit_of_measurement": "°C", "friendly_name": "Bedroom"}
    )
    hass.states.set(
        "sensor.bathroom_temp", "24", {"unit_of_measurement": "°C", "friendly_name": "Bathroom"}
    )


def create_battery_states(hass: MockHass) -> None:
    """Create mock states for battery dashboard."""
    hass.states.set(
        "sensor.phone_battery", "87", {"unit_of_measurement": "%", "friendly_name": "Phone"}
    )
    hass.states.set(
        "sensor.tablet_battery", "42", {"unit_of_measurement": "%", "friendly_name": "Tablet"}
    )
    hass.states.set(
        "sensor.watch_battery", "15", {"unit_of_measurement": "%", "friendly_name": "Watch"}
    )
    hass.states.set(
        "sensor.earbuds_battery", "100", {"unit_of_measurement": "%", "friendly_name": "AirPods"}
    )


def create_security_states(hass: MockHass) -> None:
    """Create mock states for security dashboard."""
    hass.states.set("alarm_control_panel.home", "armed_home", {"friendly_name": "Alarm"})
    hass.states.set("lock.front_door", "locked", {"friendly_name": "Front Door"})
    hass.states.set("lock.back_door", "locked", {"friendly_name": "Back Door"})
    hass.states.set("lock.garage", "unlocked", {"friendly_name": "Garage"})
    hass.states.set("binary_sensor.living_motion", "off", {"friendly_name": "Living Room"})
    hass.states.set("binary_sensor.kitchen_motion", "off", {"friendly_name": "Kitchen"})
    hass.states.set("binary_sensor.backyard_motion", "on", {"friendly_name": "Backyard"})
