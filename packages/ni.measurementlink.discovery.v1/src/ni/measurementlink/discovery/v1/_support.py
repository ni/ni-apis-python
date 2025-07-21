import msvcrt
import pathlib
import sys
import os
import typing
import winreg
import win32file
import win32con


def _open_key_file(path: str) -> typing.TextIO:
    if sys.platform == "win32":
        # Use the Win32 API to specify the share mode. Otherwise, opening the file throws
        # PermissionError due to a sharing violation. This is a workaround for
        # https://github.com/python/cpython/issues/59449
        # (Support for opening files with FILE_SHARE_DELETE on Windows).
        try:
            win32_file_handle = win32file.CreateFile(
                path,
                win32file.GENERIC_READ,
                win32file.FILE_SHARE_READ
                | win32file.FILE_SHARE_WRITE
                | win32file.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                0,
                None,
            )
        except win32file.error as e:
            raise OSError(None, e.strerror, path, e.winerror) from e

        # The CRT file descriptor takes ownership of the Win32 file handle.
        # os.O_TEXT is unnecessary because Python handles newline conversion.
        crt_file_descriptor = msvcrt.open_osfhandle(win32_file_handle.handle, os.O_RDONLY)
        win32_file_handle.Detach()

        # The Python file object takes ownership of the CRT file descriptor. Closing the Python
        # file object closes the underlying Win32 file handle.
        return os.fdopen(crt_file_descriptor, "r", encoding="utf-8-sig")
    else:
        return open(path)

def _get_nipath(name: str) -> pathlib.Path:
    if sys.platform == "win32":
        access: int = winreg.KEY_READ
        if "64" in name:
            access |= winreg.KEY_WOW64_64KEY
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\National Instruments\Common\Installer",
            access=access,
        ) as key:
            value, type = winreg.QueryValueEx(key, name)
            assert type == winreg.REG_SZ
            return pathlib.Path(value)
    else:
        raise NotImplementedError("Platform not supported")