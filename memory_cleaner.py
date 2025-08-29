import ctypes
import ctypes.wintypes
import psutil
import os
import gc
import time

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
psapi = ctypes.WinDLL("psapi", use_last_error=True)

EmptyWorkingSet = psapi.EmptyWorkingSet
EmptyWorkingSet.argtypes = [ctypes.wintypes.HANDLE]
EmptyWorkingSet.restype = ctypes.wintypes.BOOL

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
OpenProcess.restype = ctypes.wintypes.HANDLE

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
CloseHandle.restype = ctypes.wintypes.BOOL

PROCESS_ALL_ACCESS = 0x1F0FFF

def free_memory(intensity=1):
    current_pid = os.getpid()
    for _ in range(intensity):
        for proc in psutil.process_iter(['pid']):
            pid = proc.info['pid']
            if pid == current_pid:
                continue
            try:
                handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
                if handle:
                    EmptyWorkingSet(handle)
                    CloseHandle(handle)
            except Exception:
                pass
    gc.collect()

def get_memory_stats():
    mem = psutil.virtual_memory()
    compressed = getattr(mem, 'compressed', 0)
    cached = getattr(mem, 'cached', 0)
    available = getattr(mem, 'available', 0)
    return compressed, cached, available

def main_loop():
    last_stats = get_memory_stats()
    intensity = 1
    max_intensity = 300
    reset_time = 4.0  # segundos
    start_time = time.perf_counter()

    print("Starting memory optimization with variable intensity based on usage and cache...")

    while True:
        current_time = time.perf_counter()
        elapsed = current_time - start_time

        current_stats = get_memory_stats()
        compressed_diff = abs(current_stats[0] - last_stats[0])
        cached_diff = abs(current_stats[1] - last_stats[1])
        available_diff = abs(current_stats[2] - last_stats[2])

        if compressed_diff > 0 or cached_diff > 0 or available_diff > 0:
            intensity = min(intensity * 300, max_intensity)
        else:
            intensity = 1

        if elapsed >= reset_time:
            intensity = 1
            start_time = current_time

        free_memory(intensity=intensity)
        last_stats = current_stats

        time.sleep(0.1)

if __name__ == "__main__":
    main_loop()
