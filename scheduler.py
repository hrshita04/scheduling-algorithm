import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Initialize process list
processes = []

# Add process function
def add_process():
    try:
        pid = len(processes) + 1
        arrival_time = int(arrival_time_entry.get())
        burst_time = int(burst_time_entry.get())
        processes.append({"pid": pid, "arrival_time": arrival_time, "burst_time": burst_time})
        process_table.insert("", "end", values=(pid, arrival_time, burst_time))
        arrival_time_entry.delete(0, tk.END)
        burst_time_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integer values.")

# Clear processes
def clear_processes():
    processes.clear()
    process_table.delete(*process_table.get_children())

# FCFS Scheduling
def fcfs_scheduling():
    processes.sort(key=lambda x: x["arrival_time"])
    time = 0
    gantt_chart = []
    for process in processes:
        if time < process["arrival_time"]:
            gantt_chart.append({"pid": "Idle", "start": time, "end": process["arrival_time"]})
            time = process["arrival_time"]
        start_time = time
        time += process["burst_time"]
        gantt_chart.append({"pid": process["pid"], "start": start_time, "end": time})
    visualize_gantt(gantt_chart)

# SJF Scheduling
def sjf_scheduling():
    time = 0
    ready_queue = []
    gantt_chart = []
    processes.sort(key=lambda x: x["arrival_time"])
    while processes or ready_queue:
        while processes and processes[0]["arrival_time"] <= time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: x["burst_time"])
            process = ready_queue.pop(0)
            start_time = time
            time += process["burst_time"]
            gantt_chart.append({"pid": process["pid"], "start": start_time, "end": time})
        else:
            gantt_chart.append({"pid": "Idle", "start": time, "end": time + 1})
            time += 1
    visualize_gantt(gantt_chart)

# Round Robin Scheduling
def round_robin_scheduling():
    try:
        time_quantum = int(time_quantum_entry.get())
        ready_queue = []
        time = 0
        gantt_chart = []
        processes.sort(key=lambda x: x["arrival_time"])
        while processes or ready_queue:
            while processes and processes[0]["arrival_time"] <= time:
                ready_queue.append(processes.pop(0))
            if ready_queue:
                process = ready_queue.pop(0)
                start_time = time
                execute_time = min(process["burst_time"], time_quantum)
                process["burst_time"] -= execute_time
                time += execute_time
                gantt_chart.append({"pid": process["pid"], "start": start_time, "end": time})
                if process["burst_time"] > 0:
                    ready_queue.append(process)
            else:
                gantt_chart.append({"pid": "Idle", "start": time, "end": time + 1})
                time += 1
        visualize_gantt(gantt_chart)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid time quantum.")

# Visualize Gantt Chart
def visualize_gantt(gantt_chart):
    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = 1
    for block in gantt_chart:
        ax.broken_barh([(block["start"], block["end"] - block["start"])], (y_pos - 0.4, 0.8),
                       facecolors=('tab:blue' if block["pid"] != "Idle" else 'tab:gray'))
        ax.text(block["start"] + (block["end"] - block["start"]) / 2, y_pos, str(block["pid"]),
                ha='center', va='center', color='white')
    ax.set_ylim(0, 2)
    ax.set_xlim(0, gantt_chart[-1]["end"])
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Scheduling Algorithm Visualization")

frame = tk.Frame(root)
frame.pack(pady=10)

# Input Section
tk.Label(frame, text="Arrival Time").grid(row=0, column=0, padx=5, pady=5)
arrival_time_entry = tk.Entry(frame)
arrival_time_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Burst Time").grid(row=0, column=2, padx=5, pady=5)
burst_time_entry = tk.Entry(frame)
burst_time_entry.grid(row=0, column=3, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Process", command=add_process)
add_button.grid(row=0, column=4, padx=5, pady=5)

clear_button = tk.Button(frame, text="Clear Processes", command=clear_processes)
clear_button.grid(row=0, column=5, padx=5, pady=5)

# Process Table
columns = ("PID", "Arrival Time", "Burst Time")
process_table = ttk.Treeview(root, columns=columns, show="headings", height=8)
process_table.pack(pady=10)
for col in columns:
    process_table.heading(col, text=col)

# Scheduling Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

fcfs_button = tk.Button(button_frame, text="FCFS", command=fcfs_scheduling)
fcfs_button.grid(row=0, column=0, padx=10, pady=5)

sjf_button = tk.Button(button_frame, text="SJF", command=sjf_scheduling)
sjf_button.grid(row=0, column=1, padx=10, pady=5)

tk.Label(button_frame, text="Time Quantum:").grid(row=1, column=0, padx=5, pady=5)
time_quantum_entry = tk.Entry(button_frame)
time_quantum_entry.grid(row=1, column=1, padx=5, pady=5)

rr_button = tk.Button(button_frame, text="Round Robin", command=round_robin_scheduling)
rr_button.grid(row=1, column=2, padx=10, pady=5)

# Run the GUI
root.mainloop()
