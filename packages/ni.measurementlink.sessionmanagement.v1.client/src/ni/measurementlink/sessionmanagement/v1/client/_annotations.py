import socket
import sys

import win32api

from ni.measurementlink.sessionmanagement.v1.client._constants import (
    REGISTERED_HOSTNAME,
    REGISTERED_IPADDRESS,
    REGISTERED_USERNAME,
    RESERVED_HOSTNAME,
    RESERVED_IPADDRESS,
    RESERVED_USERNAME,
)


def get_machine_details() -> tuple[dict[str, str], dict[str, str]]:
    """Get the machine details for reserved and registered annotations."""
    hostname = _get_hostname()
    username = _get_username()
    ip_address = _get_ip_address()

    reserved = {
        RESERVED_HOSTNAME: hostname,
        RESERVED_USERNAME: username,
        RESERVED_IPADDRESS: ip_address,
    }

    registered = {
        REGISTERED_HOSTNAME: hostname,
        REGISTERED_USERNAME: username,
        REGISTERED_IPADDRESS: ip_address,
    }

    return reserved, registered


def remove_reservation_annotations(annotations: dict[str, str]) -> dict[str, str]:
    """Remove reserved annotations from the provided annotations."""
    reservation_keys = {
        RESERVED_HOSTNAME,
        RESERVED_USERNAME,
        RESERVED_IPADDRESS,
    }
    return {k: v for k, v in annotations.items() if k not in reservation_keys}


def _get_hostname() -> str:
    if sys.platform == "win32":
        try:
            return win32api.GetComputerName()
        except Exception:
            return ""
    else:
        raise NotImplementedError(
            f"Platform not supported: {sys.platform}. Supported platforms: win32."
        )


def _get_username() -> str:
    if sys.platform == "win32":
        try:
            return win32api.GetUserName()
        except Exception:
            return ""
    else:
        raise NotImplementedError(
            f"Platform not supported: {sys.platform}. Supported platforms: win32."
        )


def _get_ip_address() -> str:
    try:
        return socket.gethostbyname_ex("")[2][0]
    except Exception:
        return ""
