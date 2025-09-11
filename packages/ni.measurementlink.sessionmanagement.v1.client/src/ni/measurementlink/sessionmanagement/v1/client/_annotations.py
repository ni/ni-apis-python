from __future__ import annotations

import os
import socket
import sys

from ni.measurementlink.sessionmanagement.v1.annotations import (
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


def remove_reservation_annotations(annotations: dict[str, str] | None) -> dict[str, str]:
    """Remove reserved annotations from the provided annotations."""
    if annotations is None:
        return {}
    reservation_keys = {
        RESERVED_HOSTNAME,
        RESERVED_USERNAME,
        RESERVED_IPADDRESS,
    }
    return {k: v for k, v in annotations.items() if k not in reservation_keys}


def _get_hostname() -> str:
    if sys.platform == "win32":
        try:
            import win32api  # pyright: ignore[reportMissingModuleSource]

            return win32api.GetComputerName()
        except Exception:
            return ""
    else:
        return socket.gethostname()


def _get_username() -> str:
    if sys.platform == "win32":
        try:
            import win32api  # pyright: ignore[reportMissingModuleSource]

            return win32api.GetUserName()
        except Exception:
            return ""
    else:
        return os.environ.get("USER", "")


def _get_ip_address() -> str:
    try:
        ipv4_addresses = [
            info[4][0] for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)
        ]
        return str(ipv4_addresses[0]) if ipv4_addresses else ""
    except Exception:
        return ""
