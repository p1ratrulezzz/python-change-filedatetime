import os
import win32file
import win32api
from datetime import datetime, timezone
import winnt
from pytz import timezone as pytztimezone


# Variables
directory_path = r"E:\Фото и видео из Яндекс.Диска"



############################################################

def read_file_time(hFile):
    ftimes = win32file.GetFileTime(hFile)
    return ftimes

def set_file_time(hFile, ctime, mtime = None, atime = None):
    win32file.SetFileTime(hFile, ctime, mtime, atime)

def open_file(filename: str):
    hFile = win32file.CreateFile(
        filename,
        win32file.GENERIC_READ | winnt.FILE_WRITE_ATTRIBUTES,
        win32file.FILE_SHARE_READ,
        None,
        win32file.OPEN_ALWAYS,
        win32file.FILE_ATTRIBUTE_NORMAL,
        None
    )

    return hFile

def fix_filetime(filepath: str):
    filepath = os.path.normpath(filepath)
    filename = os.path.basename(filepath)
    filename_only = os.path.splitext(filename)[0]
    
    filename_only = filename_only.split('_')[0]
    dt = datetime.strptime(filename_only, "%Y-%m-%d %H-%M-%S")

    dt = pytztimezone("Europe/Moscow").localize(dt)
    dt_utc = dt.astimezone(timezone.utc)
    hFile = open_file(filepath)
    success = False
    try:
        set_file_time(hFile, dt_utc, dt_utc, dt_utc)
        success = True
    except Exception as e:
        pass
    finally:
        win32api.CloseHandle(hFile)
    return success

for root, subdirs, files in os.walk(directory_path):
    for filename in files:
        filepath = os.path.normpath(root + '/' + filename)
        fix_filetime(filepath)