import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import psutil
import time
import subprocess
import sys

# Graphing Functions
def update_plot():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    current_time = time.time()
    elapsed_time = current_time - initial_time

    cpu_x.append(elapsed_time)
    cpu_y.append(cpu)

    mem_x.append(elapsed_time)
    mem_y.append(mem)

    disk_x.append(elapsed_time)
    disk_y.append(disk)

    ax_cpu.clear()
    ax_cpu.plot(cpu_x, cpu_y, label='CPU Usage', color='blue')
    ax_cpu.set_title("CPU Usage")
    ax_cpu.set_xlabel("Time (seconds)")
    ax_cpu.set_ylabel("Usage (%)")
    ax_cpu.legend()
    ax_cpu.set_xlim(max(0, elapsed_time - 60), elapsed_time)
    ax_cpu.set_ylim(0, 100)

    ax_mem.clear()
    ax_mem.plot(mem_x, mem_y, label='Memory Usage', color='green')
    ax_mem.set_title("Memory Usage")
    ax_mem.set_xlabel("Time (seconds)")
    ax_mem.set_ylabel("Usage (%)")
    ax_mem.legend()
    ax_mem.set_xlim(max(0, elapsed_time - 60), elapsed_time)
    ax_mem.set_ylim(0, 100)

    ax_disk.clear()
    ax_disk.plot(disk_x, disk_y, label='Disk Usage', color='red')
    ax_disk.set_title("Disk Usage")
    ax_disk.set_xlabel("Time (seconds)")
    ax_disk.set_ylabel("Usage (%)")
    ax_disk.legend()
    ax_disk.set_xlim(max(0, elapsed_time - 60), elapsed_time)
    ax_disk.set_ylim(0, 100)

    canvas.draw()

    tsk.after(100, update_plot)

# Process Management Functions
def open_process_window():
    process_window = tk.Toplevel(root)
    process_window.title("Process Management")

    start_label = tk.Label(process_window, text="Enter process name to start:")
    start_label.pack()

    start_entry = tk.Entry(process_window)
    start_entry.pack()

    start_button = tk.Button(process_window, text="Start Process", command=start_process)
    start_button.pack()

    close_button = tk.Button(process_window, text="Close", command=process_window.destroy)
    close_button.pack()

def start_process():
    process_name = start_entry.get()
    try:
        if platform == "win32":
            subprocess.Popen(["start", "", process_name], shell=True)
        else:
            subprocess.Popen([process_name])
    except Exception as e:
        print(f"Error starting process: {e}")

def close_application():
    tsk.destroy()

# Main Function
if __name__ == "__main__":
    platform = sys.platform  # Detect the current platform
    tsk = tk.Tk()
    tsk.title("Task Manager")

    # Create Graphs
    fig, (ax_cpu, ax_mem, ax_disk) = plt.subplots(nrows=3, ncols=1, figsize=(8, 10), sharex=True)

    # Initialize data arrays (cpu_x, cpu_y, mem_x, mem_y, disk_x, disk_y)
    cpu_x = []
    cpu_y = []
    mem_x = []
    mem_y = []
    disk_x = []
    disk_y = []
    initial_time = time.time()

    # Create Matplotlib canvas
    canvas = FigureCanvasTkAgg(fig, master=tsk)
    canvas.get_tk_widget().pack()

    # Open Process Management Window Button
    process_button = tk.Button(tsk, text="Open Process Management", command=open_process_window)
    process_button.pack()

    # Update function for graphs
    tsk.after(100, update_plot)  # Set update rate to 100 milliseconds

    close_button = tk.Button(tsk, text="Close", command=close_application)
    close_button.pack()

    tsk.mainloop()
