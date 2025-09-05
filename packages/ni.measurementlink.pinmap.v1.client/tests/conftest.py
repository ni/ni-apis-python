"""Pytest configuration file."""

from __future__ import annotations

import pathlib
import sys
from collections.abc import Generator

import grpc
import pytest
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni.measurementlink.discovery.v1.client._support import (
    _get_registration_json_file_path,
)
from ni.measurementlink.measurement.v1 import (
    measurement_service_pb2_grpc as v1_measurement_service_pb2_grpc,
)
from ni.measurementlink.measurement.v2 import (
    measurement_service_pb2_grpc as v2_measurement_service_pb2_grpc,
)
from ni.measurementlink.sessionmanagement.v1.client import SessionManagementClient
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurementlink.pinmap.v1.client import PinMapClient
from tests.utilities.discovery_service_process import DiscoveryServiceProcess


@pytest.fixture(scope="module")
def pin_map_directory(test_assets_directory: pathlib.Path) -> pathlib.Path:
    """Test fixture that returns the pin map directory."""
    return test_assets_directory / "unit" / "pin_map"


@pytest.fixture(scope="module")
def test_assets_directory() -> pathlib.Path:
    """Gets path to test_assets directory."""
    return pathlib.Path(__file__).parent / "assets"


@pytest.fixture
def stub_v1(grpc_channel: grpc.Channel) -> v1_measurement_service_pb2_grpc.MeasurementServiceStub:
    """Test fixture that creates a MeasurementService v1 stub."""
    return v1_measurement_service_pb2_grpc.MeasurementServiceStub(grpc_channel)


@pytest.fixture
def stub_v2(grpc_channel: grpc.Channel) -> v2_measurement_service_pb2_grpc.MeasurementServiceStub:
    """Test fixture that creates a MeasurementService v2 stub."""
    return v2_measurement_service_pb2_grpc.MeasurementServiceStub(grpc_channel)


@pytest.fixture(scope="session")
def discovery_service_process() -> Generator[DiscoveryServiceProcess]:
    """Test fixture that creates discovery service process."""
    if sys.platform != "win32":
        pytest.skip(f"Platform {sys.platform} is not supported for discovery service tests.")

    try:
        registration_json_file_exists = _get_registration_json_file_path().exists()
    except FileNotFoundError:  # registry key not found
        registration_json_file_exists = False
    if not registration_json_file_exists:
        pytest.skip("Registration file not found. Ensure the Measurement Plug-In SDK is installed.")

    with DiscoveryServiceProcess() as proc:
        yield proc


@pytest.fixture(scope="session")
def grpc_channel_pool() -> Generator[GrpcChannelPool]:
    """Test fixture that creates a gRPC channel pool."""
    with GrpcChannelPool() as grpc_channel_pool:
        yield grpc_channel_pool


@pytest.fixture
def discovery_client(
    discovery_service_process: DiscoveryServiceProcess, grpc_channel_pool: GrpcChannelPool
) -> DiscoveryClient:
    """Test fixture that creates a discovery client."""
    return DiscoveryClient(grpc_channel_pool=grpc_channel_pool)


@pytest.fixture
def pin_map_client(
    discovery_client: DiscoveryClient, grpc_channel_pool: GrpcChannelPool
) -> PinMapClient:
    """Test fixture that creates a pin map client."""
    return PinMapClient(discovery_client=discovery_client, grpc_channel_pool=grpc_channel_pool)


@pytest.fixture
def session_management_client(
    discovery_client: DiscoveryClient, grpc_channel_pool: GrpcChannelPool
) -> SessionManagementClient:
    """Test fixture that creates a session management client."""
    return SessionManagementClient(
        discovery_client=discovery_client, grpc_channel_pool=grpc_channel_pool
    )
