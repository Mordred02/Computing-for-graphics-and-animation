# guis.py
import tkinter as tk
from tkinter import colorchooser

def show_gui(parameter_queue):
    def update_parameters():
        params = {
            'release_interval': float(slider_frequency.get()),
            'obj_quantity': int(slider_quantity.get()),
            'sphere_color': sphere_color,
            'sphere_restitution': float(entry_sphere_restitution.get()),
            'ground_restitution': float(entry_ground_restitution.get())
        }
        parameter_queue.put(params)
        window.destroy()
    
    def choose_color():
        nonlocal sphere_color
        color_code = colorchooser.askcolor(title="Choose sphere color")
        if color_code[1]:
            sphere_color = color_code[1]

    window = tk.Tk()
    window.title("3D Viewer Controls")

    tk.Label(window, text="Ball Release Frequency (seconds):").pack()
    slider_frequency = tk.Scale(window, from_=0.05, to=3.0, resolution=0.01, orient='horizontal', length=300)
    slider_frequency.set(1.0)
    slider_frequency.pack()

    tk.Label(window, text="Number of Balls Released:").pack()
    slider_quantity = tk.Scale(window, from_=1, to=10, orient='horizontal', length=300)
    slider_quantity.set(1)
    slider_quantity.pack()

    tk.Label(window, text="Sphere Restitution Coefficient:").pack()
    entry_sphere_restitution = tk.Entry(window)
    entry_sphere_restitution.insert(0, "0.8")
    entry_sphere_restitution.pack()

    tk.Label(window, text="Ground Restitution Coefficient:").pack()
    entry_ground_restitution = tk.Entry(window)
    entry_ground_restitution.insert(0, "0.8")
    entry_ground_restitution.pack()

    sphere_color = '#FFFFFF'  # default white
    tk.Button(window, text="Choose Sphere Color", command=choose_color).pack()
    tk.Button(window, text="Update Settings and Start Simulation", command=update_parameters).pack()

    window.mainloop()
