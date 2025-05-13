import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image
from colour import Color
from app.utils import color_picker, generate_points, version, load_config
from app.knn_canvas import canvas_determine

config = load_config()

# Canvas dimensions
WIDTH = config['canvas']['width']
HEIGHT = config['canvas']['height']
BORDER_XL = config['canvas']['border_x_low']
BORDER_YL = config['canvas']['border_y_low']
BORDER_XH = config['canvas']['border_x_high']
BORDER_YH = config['canvas']['border_y_high']

# KNN Settings
resolution = config['knn']['resolution']
k = config['knn']['default_k']
numLabels = config['knn']['default_num_labels']
numPoints = config['knn']['default_num_points']

# GUI style
BG_COLOR = config['gui']['bg_color']
ENTRY_WIDTH = config['gui']['entry_width']
BUTTON_COLOR = config['gui']['button_color']
BUTTON_ACTIVE_COLOR = config['gui']['button_active_color']

def main():
    global FNumL, FNumP, FKSet, pointSpace, select_points, distType, numLabels, numPoints

    select_points = generate_points(BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL, numLabels, numPoints)

    base = tk.Tk()
    base.resizable(False, False)
    base.title("tk2NN")
    base.geometry(f"{WIDTH}x{HEIGHT}")

    # Set background image
    bg_image = tk.PhotoImage(file="assets/bg.png")
    bg_label = tk.Label(base, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    # Style the update button
    style = ttk.Style()
    style.configure("Custom.TButton",
                    background=BUTTON_COLOR,
                    foreground="black",
                    padding=5)

    distType = tk.IntVar(value=1)

    pointSpace = tk.Canvas(base, width=BORDER_XH - BORDER_XL, height=BORDER_YH - BORDER_YL,
                           borderwidth=4, relief=tk.SUNKEN, background='black', cursor='dot')
    pointSpace.grid(row=0, column=0, columnspan=3, padx=(BORDER_XL, 5), pady=(BORDER_YL, 5))

    def update_point_space():
        width = BORDER_XH - BORDER_XL
        height = BORDER_YH - BORDER_YL
        canvas, _ = canvas_determine(k, distType.get(), width, height, select_points)
        colors = color_picker(select_points)

        img = tk.PhotoImage(width=width, height=height)

        color_map = {}
        for label, color in colors.items():
            c = Color(color.hex_l)
            c.saturation = (c.saturation + 1.0) / 2.0
            color_map[label] = c.hex_l

        for y in range(height):
            row = "{" + " ".join(
                color_map.get(canvas[y][x], "#000000") for x in range(width)
            ) + "}"
            img.put(row, to=(0, y))

        pointSpace.delete("all")
        pointSpace.create_image(0, 0, anchor=tk.NW, image=img)
        pointSpace.image = img

        for point in select_points:
            pointX, pointY = point[0]
            pointSpace.create_rectangle(
                pointX - resolution * 2, pointY - resolution * 2,
                pointX + resolution * 2, pointY + resolution * 2,
                fill=colors[point[1]].hex_l
            )

    def update_input(event=None):
        global k, numLabels, numPoints, select_points
        try:
            new_labels = int(FNumL.get())
            new_points = int(FNumP.get())
            new_k = int(FKSet.get())
            changed = (numLabels != new_labels) or (numPoints != new_points)
            numLabels, numPoints, k = new_labels, new_points, new_k
            if changed:
                select_points = generate_points(BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL, numLabels, numPoints)
            update_point_space()
        except ValueError:
            print("Invalid input.")

    def clear_point_space(event=None):
        global select_points
        select_points = []
        pointSpace.delete("all")

    # Distance type radio buttons
    typeSpace = ttk.Frame(base)
    typeSpace.grid(row=0, column=3, rowspan=2, pady=(5, 5))
    ttk.Radiobutton(typeSpace, text="Euclidean", variable=distType, value=1, command=update_point_space).pack(anchor=tk.W)
    ttk.Radiobutton(typeSpace, text="Manhattan", variable=distType, value=2, command=update_point_space).pack(anchor=tk.E)

    # Entry fields and update button
    labelSpace = ttk.Frame(base)
    labelSpace.grid(row=1, column=0, columnspan=2, padx=25)
    FNumL = ttk.Entry(labelSpace, width=ENTRY_WIDTH)
    FNumP = ttk.Entry(labelSpace, width=ENTRY_WIDTH)
    FKSet = ttk.Entry(labelSpace, width=ENTRY_WIDTH)
    UpdtB = ttk.Button(labelSpace, text="Update", style="Custom.TButton")
    FNumL.insert(0, str(numLabels))
    FNumP.insert(0, str(numPoints))
    FKSet.insert(0, str(k))
    FNumL.pack(side=tk.LEFT)
    FNumP.pack(side=tk.LEFT)
    FKSet.pack(side=tk.LEFT)
    UpdtB.pack(side=tk.LEFT)

    for entry in (FNumL, FNumP, FKSet):
        entry.bind("<FocusIn>", lambda e, ent=entry: ent.delete(0, tk.END))

    FNumL.bind("<Return>", update_input)
    UpdtB.bind("<Button-1>", update_input)
    pointSpace.bind("<Button-2>", clear_point_space)

    update_point_space()
    base.mainloop()
