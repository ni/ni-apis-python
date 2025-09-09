from unittest.mock import Mock

import grpc
import ni.datamonikers.v1.data_moniker_pb2 as data_moniker_types
import pytest
from ni.datamonikers.v1.data_moniker_pb2_grpc import (
    MonikerServiceStub,
)
from pytest_mock import MockerFixture

from ni.datamonikers.v1.client import MonikerClient


def test__begin_sideband_stream__request_and_response_pass_through(
    moniker_client: MonikerClient, moniker_stub: Mock
) -> None:
    client_request = data_moniker_types.BeginMonikerSidebandStreamRequest()
    client_request.strategy = data_moniker_types.SidebandStrategy.GRPC
    stub_response = data_moniker_types.BeginMonikerSidebandStreamResponse()
    stub_response.strategy = data_moniker_types.SidebandStrategy.GRPC
    moniker_stub.BeginSidebandStream.return_value = stub_response

    client_response = moniker_client.begin_sideband_stream(client_request)

    moniker_stub.BeginSidebandStream.assert_called_once()
    stub_request = moniker_stub.BeginSidebandStream.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__stream_read__request_and_response_pass_through(
    moniker_client: MonikerClient, moniker_stub: Mock
) -> None:
    client_request = data_moniker_types.MonikerList()
    read_moniker = client_request.read_monikers.add()
    read_moniker.service_location = "http://localhost:8080"
    stub_response_iter = [
        data_moniker_types.MonikerReadResult(),
        data_moniker_types.MonikerReadResult(),
    ]
    moniker_stub.StreamRead.return_value = iter(stub_response_iter)

    client_response = moniker_client.stream_read(client_request)
    response_list = list(client_response)

    moniker_stub.StreamRead.assert_called_once()
    stub_request = moniker_stub.StreamRead.call_args[0][0]
    assert stub_request == client_request
    assert len(response_list) == 2


def test__stream_write__request_and_response_pass_through(
    moniker_client: MonikerClient, moniker_stub: Mock
) -> None:
    client_requests = [
        data_moniker_types.MonikerWriteRequest(),
        data_moniker_types.MonikerWriteRequest(),
    ]
    stub_response_iter = [
        data_moniker_types.StreamWriteResponse(),
        data_moniker_types.StreamWriteResponse(),
    ]
    moniker_stub.StreamWrite.return_value = iter(stub_response_iter)

    client_response = moniker_client.stream_write(iter(client_requests))
    response_list = list(client_response)

    moniker_stub.StreamWrite.assert_called_once()
    stub_request_iter = moniker_stub.StreamWrite.call_args[0][0]
    assert len(list(stub_request_iter)) == 2
    assert len(response_list) == 2


def test__stream_read_write__request_and_response_pass_through(
    moniker_client: MonikerClient, moniker_stub: Mock
) -> None:
    client_requests = [
        data_moniker_types.MonikerWriteRequest(),
        data_moniker_types.MonikerWriteRequest(),
    ]
    stub_response_iter = [
        data_moniker_types.MonikerReadResult(),
        data_moniker_types.MonikerReadResult(),
    ]
    moniker_stub.StreamReadWrite.return_value = iter(stub_response_iter)

    client_response = moniker_client.stream_read_write(iter(client_requests))
    response_list = list(client_response)

    moniker_stub.StreamReadWrite.assert_called_once()
    stub_request_iter = moniker_stub.StreamReadWrite.call_args[0][0]
    assert len(list(stub_request_iter)) == 2
    assert len(response_list) == 2


def test__read_from_moniker__request_and_response_pass_through(
    moniker_client: MonikerClient, moniker_stub: Mock
) -> None:
    client_request = data_moniker_types.Moniker()
    client_request.service_location = "location"
    stub_response = data_moniker_types.ReadFromMonikerResult()
    stub_response.value.type_url = "type_url"
    moniker_stub.ReadFromMoniker.return_value = stub_response

    client_response = moniker_client.read_from_moniker(client_request)

    moniker_stub.ReadFromMoniker.assert_called_once()
    stub_request = moniker_stub.ReadFromMoniker.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__write_to_moniker__request_and_response_pass_through(
    moniker_client: MonikerClient, moniker_stub: Mock
) -> None:
    client_request = data_moniker_types.WriteToMonikerRequest()
    client_request.moniker.service_location = "location"

    moniker_client.write_to_moniker(client_request)

    moniker_stub.WriteToMoniker.assert_called_once()
    stub_request = moniker_stub.WriteToMoniker.call_args[0][0]
    assert stub_request == client_request


@pytest.fixture
def moniker_client(
    mocker: MockerFixture,
    moniker_stub: Mock,
) -> MonikerClient:
    """Create a Client with a mock MonikerServiceStub."""
    mocker.patch(
        "ni.datamonikers.v1.client.MonikerClient._get_stub",
        return_value=moniker_stub,
    )
    client = MonikerClient(service_location="not_used_service_location")
    return client


@pytest.fixture
def moniker_stub(mocker: MockerFixture) -> Mock:
    """Create a mock MonikerServiceStub."""
    stub = mocker.create_autospec(MonikerServiceStub)
    stub.BeginSidebandStream = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.StreamRead = mocker.create_autospec(grpc.UnaryStreamMultiCallable)
    stub.StreamWrite = mocker.create_autospec(grpc.StreamStreamMultiCallable)
    stub.StreamReadWrite = mocker.create_autospec(grpc.StreamStreamMultiCallable)
    stub.ReadFromMoniker = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.WriteToMoniker = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    return stub
