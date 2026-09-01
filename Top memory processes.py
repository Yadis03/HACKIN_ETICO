"""
Top RAM-consuming processes viewer.

Lists the system's running processes sorted by memory usage,
showing the ones consuming the most RAM.

Required installation:
    pip install psutil

Usage:
    python top_memory_processes.py
"""

import psutil
import time


# ----------------------------------------------------------------------
# 1. COLLECT PROCESS INFORMATION
# ----------------------------------------------------------------------
def get_process_list() -> list[dict]:
    """
    Iterates over all running processes and collects their
    PID, name, memory usage (in MB and %), and CPU usage.
    Processes that can't be accessed (permission denied, already
    terminated, etc.) are simply skipped.
    """
    process_list = []

    for process in psutil.process_iter(["pid", "name", "memory_info", "memory_percent", "cpu_percent"]):
        try:
            info = process.info
            memory_mb = info["memory_info"].rss / (1024 * 1024)  # bytes -> MB

            process_list.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory_mb": memory_mb,
                "memory_percent": info["memory_percent"],
                "cpu_percent": info["cpu_percent"],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes that disappeared or can't be read
            continue

    return process_list


# ----------------------------------------------------------------------
# 2. SORT AND FILTER
# ----------------------------------------------------------------------
def get_top_memory_processes(limit: int = 10) -> list[dict]:
    """Returns the top N processes sorted by RAM usage (descending)."""
    processes = get_process_list()
    sorted_processes = sorted(processes, key=lambda p: p["memory_mb"], reverse=True)
    return sorted_processes[:limit]


# ----------------------------------------------------------------------
# 3. DISPLAY RESULTS
# ----------------------------------------------------------------------
def print_process_table(processes: list[dict]):
    """Prints a formatted table with the process information."""
    header = f"{'PID':<8}{'NAME':<30}{'RAM (MB)':<12}{'RAM (%)':<10}{'CPU (%)':<10}"
    print(header)
    print("-" * len(header))

    for process in processes:
        print(
            f"{process['pid']:<8}"
            f"{process['name'][:28]:<30}"
            f"{process['memory_mb']:<12.2f}"
            f"{process['memory_percent']:<10.2f}"
            f"{process['cpu_percent']:<10.2f}"
        )


def print_system_summary():
    """Prints an overview of total and used system memory."""
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024 ** 3)
    used_gb = memory.used / (1024 ** 3)
    available_gb = memory.available / (1024 ** 3)

    print("--- SYSTEM MEMORY SUMMARY ---")
    print(f"Total memory:     {total_gb:.2f} GB")
    print(f"Used memory:      {used_gb:.2f} GB ({memory.percent}%)")
    print(f"Available memory: {available_gb:.2f} GB\n")


# ----------------------------------------------------------------------
# 4. MAIN PROGRAM (interactive menu)
# ----------------------------------------------------------------------
def main():
    while True:
        print("\n--- TOP MEMORY PROCESSES ---")
        print("1. Show top RAM-consuming processes")
        print("2. Show system memory summary")
        print("3. Monitor continuously (refresh every 3 seconds)")
        print("4. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            try:
                limit = int(input("How many processes to show? (default 10): ") or 10)
            except ValueError:
                limit = 10

            print_system_summary()
            top_processes = get_top_memory_processes(limit)
            print_process_table(top_processes)

        elif option == "2":
            print_system_summary()

        elif option == "3":
            try:
                limit = int(input("How many processes to show? (default 10): ") or 10)
            except ValueError:
                limit = 10

            print("Press Ctrl+C to stop monitoring.\n")
            try:
                while True:
                    print("\033c", end="")  # clear terminal screen
                    print_system_summary()
                    top_processes = get_top_memory_processes(limit)
                    print_process_table(top_processes)
                    time.sleep(3)
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")

        elif option == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()