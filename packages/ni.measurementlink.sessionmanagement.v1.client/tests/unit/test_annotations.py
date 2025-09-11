from ni.measurementlink.sessionmanagement.v1.annotations import (
    REGISTERED_HOSTNAME,
    REGISTERED_IPADDRESS,
    REGISTERED_USERNAME,
    RESERVED_HOSTNAME,
    RESERVED_IPADDRESS,
    RESERVED_USERNAME,
)

from ni.measurementlink.sessionmanagement.v1.client import _annotations


def test___machine_details___get_machine_details___returns_reserved_and_registered() -> None:
    reserved, registered = _annotations.get_machine_details()
    assert RESERVED_HOSTNAME in reserved
    assert RESERVED_USERNAME in reserved
    assert RESERVED_IPADDRESS in reserved
    assert REGISTERED_HOSTNAME in registered
    assert REGISTERED_USERNAME in registered
    assert REGISTERED_IPADDRESS in registered
    for v in reserved.values():
        assert isinstance(v, str)
    for v in registered.values():
        assert isinstance(v, str)


def test___annotations_dict_with_reserved_keys___remove_reservation_annotations___removes_reserved_keys() -> (
    None
):
    annotations = {
        RESERVED_HOSTNAME: "host1",
        RESERVED_USERNAME: "user",
        RESERVED_IPADDRESS: "ip",
        REGISTERED_HOSTNAME: "host2",
    }
    result = _annotations.remove_reservation_annotations(annotations)
    assert RESERVED_HOSTNAME not in result
    assert RESERVED_USERNAME not in result
    assert RESERVED_IPADDRESS not in result
    assert REGISTERED_HOSTNAME in result
    assert result[REGISTERED_HOSTNAME] == "host2"


def test___machine_details___get_machine_details___values_not_empty() -> None:
    reserved, registered = _annotations.get_machine_details()
    for v in reserved.values():
        assert v != ""
    for v in registered.values():
        assert v != ""
