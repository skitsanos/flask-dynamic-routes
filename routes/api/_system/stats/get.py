"""
Returns the CPU and memory usage of the current process.
"""
import os
import psutil


def handler():
    """
    Returns a dictionary containing the CPU and memory usage of the current process.
    """
    process = psutil.Process(os.getpid())
    cpu_percent = process.cpu_percent()
    mem_info = process.memory_info()
    mem_percent = mem_info.rss / (1024 ** 2)  # Convert from bytes to MB

    return {
        "cpu": cpu_percent,
        "memory": mem_percent
    }
