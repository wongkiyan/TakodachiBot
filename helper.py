import psutil
from src.utils.datetime_utils import format_datetime
import sys

def get_pyw_pid_list(app_name):
    pyw_pid_list = []
    for process in psutil.process_iter(['pid', 'cmdline']):
        command_line = process.info.get('cmdline', [])
        if not command_line:
            continue
        if command_line[-1].lower() == app_name:
            pyw_pid_list.append((process.info['pid']))
    return pyw_pid_list

def print_english_details(app_name, process):
    print(f"{app_name}")
    print("=" * 30)
    print(f"Status: {process.status()}")
    print()
    print(f"Command Line: {' '.join(process.cmdline())}")
    print()
    print(f"Create Time: {format_datetime(process.create_time())}")
    print()
    print(f"CPU Usage (%): {process.cpu_percent()}%")
    print(f"Memory Usage (%): {process.memory_percent()}%")
    print()
    print(f"Number of Threads: {process.num_threads()}")
    print(f"Number of Handles: {process.num_handles()}")
    # print(f"Name: {process.name()}")
    # print(f"PID: {process.pid}")
    # print(f"Parent PID: {process.ppid()}")
    # print(f"Executable: {process.exe()}")
    print("=" * 30)
    print("")

def print_process_data_list(app_name, pyw_pid_list):
    if not pyw_pid_list:
        print(
            f"No running python processes with the name {app_name}.")
        return

    # 遍歷所有進程資料
    for pid in pyw_pid_list:
        try:
            # 根據PID獲取進程
            process = psutil.Process(pid)

            # 列印進程詳細信息
            print_english_details(app_name, process)

        except psutil.NoSuchProcess:
            print(f"沒有PID為{pid}的行程")
        except psutil.AccessDenied:
            print(f"拒絕存取PID為{pid}的程序")

def show_app_status():
    app_name = "takodachi.pyw"
    pyw_pid_list = get_pyw_pid_list(app_name)
    print_process_data_list(app_name, pyw_pid_list)

if __name__ == "__main__":
    request_functions = {
        "STATUS": show_app_status,
    }
    if len(sys.argv) >= 2:
        request_type = sys.argv[1].upper()
        function_to_execute = request_functions.get(request_type)
        function_to_execute() if function_to_execute else print("Request type not found: {request_type}. Exiting.")