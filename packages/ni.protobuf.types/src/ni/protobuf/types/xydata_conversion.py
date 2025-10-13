"""Methods to convert to and from DoubleXYData protobuf messages."""

from __future__ import annotations

import numpy as np
from nitypes.xy_data import XYData

import ni.protobuf.types.xydata_pb2 as xydata_pb2
from ni.protobuf.types.extended_property_conversion import (
    extended_properties_from_protobuf,
    extended_properties_to_protobuf,
)


def float64_xydata_to_protobuf(value: XYData[np.float64], /) -> xydata_pb2.DoubleXYData:
    """Convert a XYData python object to a protobuf xydata_pb2.DoubleXYData."""
    attributes = extended_properties_to_protobuf(value.extended_properties)
    xydata_message = xydata_pb2.DoubleXYData(
        x_data=value.x_data,
        y_data=value.y_data,
        attributes=attributes,
    )
    return xydata_message


def float64_xydata_from_protobuf(message: xydata_pb2.DoubleXYData, /) -> XYData[np.float64]:
    """Convert the protobuf xydata_pb2.DoubleXYData to a Python XYData."""
    xydata = XYData.from_arrays_1d(
        x_array=message.x_data,
        y_array=message.y_data,
        dtype=np.float64,
    )

    # Transfer attributes to extended_properties
    extended_properties_from_protobuf(message.attributes, xydata.extended_properties)

    return xydata
