import asyncio

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_TOKEN, CONF_USER_AGENT, DEFAULT_USER_AGENT
from .api import ExtelUmiiAPI
from .coordinator import ExtelGateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = ExtelUmiiAPI(
        entry.data[CONF_EMAIL],
        entry.data[CONF_PASSWORD],
        entry.data.get(CONF_DEVICE_ID),
        entry.data.get(CONF_DEVICE_TOKEN),
        entry.data.get(CONF_USER_AGENT, DEFAULT_USER_AGENT),
    )

    try:
        logged_in = await api.login()
    except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as err:
        raise ConfigEntryNotReady(
            f"Impossible de joindre l'API Umii : {err}"
        ) from err

    if not logged_in:
        if api.last_login_status in (401, 403):
            raise ConfigEntryAuthFailed("Identifiants Umii refusés")
        raise ConfigEntryNotReady(
            f"Connexion Umii échouée (HTTP {api.last_login_status})"
        )

    coordinator = ExtelGateCoordinator(hass, api, entry.data["gate_id"])
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["cover", "button", "binary_sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["cover", "button", "binary_sensor"]
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok