import tkinter as tk
from tkinter import ttk, colorchooser
import matplotlib.pyplot as plt
import numpy as np

# Stats and scale
labels = ["Power", "Speed", "Range", "Durability", "Precision", "Potential"]
stats_scale = ["N/a", "F", "E", "D", "C", "B", "A", "A+", "S", "EN", "CC", "RE", "INF"]
max_rank = len(stats_scale) - 1

def rank_to_value(rank):
    if rank == "INF":
        return 13.25  # Visibly past RE
    elif rank == "RE":
        return 11
    elif rank in stats_scale:
        return stats_scale.index(rank)
    return 0

def plot_stand_chart(stat_ranks, name="Your Stand", line_color="purple", fill_color="purple", use_rainbow=True, title_color="purple"):
    plt.close('all')  # Ensure no duplicates

    values = [rank_to_value(r) for r in stat_ranks]
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    has_inf = "INF" in stat_ranks

    # Set visible ring max: start with S+ (index 8), INF forces RE (index 11)
    max_value = max([rank_to_value(r) for r in stat_ranks if r != "INF"], default=8)
    limit = max(max_value, 11) if has_inf else max(max_value, 8)
    ylim = limit + (2 if has_inf else 0)

    rgrid_labels = [stats_scale[i] if i < len(stats_scale) else "" for i in range(limit + 1)]

    fig_size = (8, 8) if has_inf else (6, 6)
    fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(polar=True))

    if has_inf and use_rainbow:
        cmap = plt.cm.hsv
        rainbow = cmap(np.linspace(0, 1, len(values) - 1))
        for i in range(len(values) - 1):
            ax.plot(angles[i:i+2], values[i:i+2], color=rainbow[i], linewidth=3)
        fill_color = (1.0, 0.5, 1.0, 0.5)
    else:
        ax.plot(angles, values, color=line_color, linewidth=2)

    ax.fill(angles, values, color=fill_color, alpha=0.4)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_rgrids(range(0, limit + 1), rgrid_labels, angle=0)
    ax.set_ylim(0, ylim)

    ax.spines['polar'].set_visible(False)
    fig.subplots_adjust(top=0.9, bottom=0.05)

    plt.title(name, size=20, color=title_color)
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Stand Stat Chart Generator")

entries = {}
tk.Label(root, text="Stand Name:").grid(row=0, column=0)
stand_name_entry = tk.Entry(root)
stand_name_entry.grid(row=0, column=1)

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i+1, column=0)
    cb = ttk.Combobox(root, values=stats_scale, state="readonly")
    cb.set("C")
    cb.grid(row=i+1, column=1)
    entries[label] = cb

def pick_line_color():
    color = colorchooser.askcolor(title="Choose Line Color")
    if color[1]:
        line_color_entry.delete(0, tk.END)
        line_color_entry.insert(0, color[1])

def pick_fill_color():
    color = colorchooser.askcolor(title="Choose Fill Color")
    if color[1]:
        fill_color_entry.delete(0, tk.END)
        fill_color_entry.insert(0, color[1])

def pick_title_color():
    color = colorchooser.askcolor(title="Choose Title Color")
    if color[1]:
        title_color_entry.delete(0, tk.END)
        title_color_entry.insert(0, color[1])

# Line color
tk.Label(root, text="Line Color (hex or name):").grid(row=7, column=0)
line_color_entry = tk.Entry(root)
line_color_entry.insert(0, "#800080")
line_color_entry.grid(row=7, column=1)
tk.Button(root, text="Pick", command=pick_line_color).grid(row=7, column=2)

# Fill color
tk.Label(root, text="Fill Color (hex or name):").grid(row=8, column=0)
fill_color_entry = tk.Entry(root)
fill_color_entry.insert(0, "#DA70D6")
fill_color_entry.grid(row=8, column=1)
tk.Button(root, text="Pick", command=pick_fill_color).grid(row=8, column=2)

# Title color
tk.Label(root, text="Title Color (hex or name):").grid(row=9, column=0)
title_color_entry = tk.Entry(root)
title_color_entry.insert(0, "#800080")
title_color_entry.grid(row=9, column=1)
tk.Button(root, text="Pick", command=pick_title_color).grid(row=9, column=2)

# Rainbow toggle
rainbow_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Enable Rainbow for INF", variable=rainbow_var).grid(row=10, column=0, columnspan=3)

def generate_chart():
    try:
        stat_values = [entries[label].get() for label in labels]
        stand_name = stand_name_entry.get() or "Unnamed Stand"
        line_color = line_color_entry.get()
        fill_color = fill_color_entry.get()
        title_color = title_color_entry.get()
        use_rainbow = rainbow_var.get()
        plot_stand_chart(stat_values, stand_name, line_color, fill_color, use_rainbow, title_color)
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while generating the chart: \nCheck the # HexCode it should be 0-9 & a-f max of 6 digits ")


tk.Button(root, text="Generate Chart", command=generate_chart).grid(row=11, column=0, columnspan=3, pady=10)

root.mainloop()