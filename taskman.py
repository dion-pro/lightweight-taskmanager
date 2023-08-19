import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import psutil
import time

try:
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    import psutil
    import time
except ImportError as e:
    print(f"Error importing module: {e}")
    print("Please make sure you have all the required modules installed.")
    exit(1)

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

    tsk.after(1000, update_plot)

def close_application():
    tsk.destroy()

if __name__ == "__main__":
    tsk = tk.Tk()
    tsk.title("Taskman")

    fig, (ax_cpu, ax_mem, ax_disk) = plt.subplots(nrows=3, ncols=1, figsize=(8, 10), sharex=True)

    cpu_x = []
    cpu_y = []

    mem_x = []
    mem_y = []

    disk_x = []
    disk_y = []

    initial_time = time.time()

    canvas = FigureCanvasTkAgg(fig, master=tsk)
    canvas.get_tk_widget().pack()

    plt.subplots_adjust(hspace=0.7, top=0.92, bottom=0.08)

    button_frame = tk.Frame(tsk)
    close_button = tk.Button(button_frame, text="Close", command=close_application)

    def toggle_button():
        if close_button.winfo_ismapped():
            close_button.pack_forget()
        else:
            close_button.pack()

    toggle_button_button = tk.Button(tsk, text="Toggle Close Button", command=toggle_button)
    toggle_button_button.pack(pady=10)

    tsk.after(1000, update_plot)

    try:
        tsk.mainloop()
    except KeyboardInterrupt:
        tsk.quit()
        print("INTERRUPTED!")
