"""grpc_generator package."""

import warnings

warnings.filterwarnings(
    action="ignore",
    category=UserWarning,
    module=r"^grpc_tools",
)  # grpc_tools\protoc.py:21: UserWarning: pkg_resources is deprecated as an API
