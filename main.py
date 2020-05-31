import time
from   PIL       import Image
from   colour    import Color
from   random    import random, randint
from   general   import colorPicker, generatePoints
from   tkinter   import *
from   canvasDev import canvasDetermine

HEIGHT     = 520
WIDTH      = 540

BORDER_XL  =  15
BORDER_YL  =  15
BORDER_XH  = 415
BORDER_YH  = 415
numLabels  =   3
numPoints  =   9
resolution =   1
k          =   1

def clearPointSpace(event):
    global selectPoints
    selectPoints = []
    pointSpace.delete(ALL)

def updateInput(event):
    global numLabels, numPoints, selectPoints, k
    nLChange = False
    nPChange = False
    nKChange = False
    try:
        nLChange  = not (numLabels == int(FNumL.get()))
        numLabels = int(FNumL.get())
    except Exception:
        pass
    try:
        nPChange  = not (numPoints == int(FNumP.get()))
        numPoints = int(FNumP.get())
    except Exception:
        pass
    try:
        nKChange  = not (k == int(FKSet.get()))
        k         = int(FKSet.get())
    except Exception:
        pass
    FNumL.delete(0, END)
    FNumP.delete(0, END)
    FKSet.delete(0, END)
    FNumL.insert(0, str(numLabels))
    FNumP.insert(0, str(numPoints))
    FKSet.insert(0, str(k))
    if nLChange or nPChange:
        selectPoints = generatePoints(BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL, numLabels, numPoints)
    updatePointSpace()

def bindButtons():
    pointSpace.delete("all")
    updatePointSpace()

def updatePointSpace():
    (canvas, error) = canvasDetermine(k, distType.get(), BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL, selectPoints)
    colors          = colorPicker(selectPoints)

    for y in range(resolution, BORDER_YH - BORDER_YL + resolution, resolution*2):
        for x in range(resolution, BORDER_XH - BORDER_XL + resolution, resolution*2):
            try:
                color = colors[canvas[y][x]]
            except Exception:
                color = Color("#000000")
            color.saturation = (color.saturation + 1.0)/2.0
            pointSpace.create_rectangle(x - resolution, y - resolution, x + resolution, y + resolution, fill = color)
    for point in selectPoints:
        pointX, pointY = point[0]
        pointSpace.create_rectangle(pointX - resolution*2, pointY - resolution*2, pointX + resolution*2, pointY + resolution*2, fill = colors[point[1]])

base = Tk()
base.resizable(width = False, height = False)
base.title("tk2NN")
base.configure(bg = 'grey')
base.geometry(str(WIDTH) + "x" + str(HEIGHT))

distType = IntVar()
distType.set(1)

selectPoints = generatePoints(BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL, numLabels, numPoints)

background_image = PhotoImage(file = './bg.png')
background_label = Label(base, image = background_image)
background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

pointSpace = Canvas(base, width = BORDER_XH - BORDER_XL, height = BORDER_YH - BORDER_YL, borderwidth = 4, relief = SUNKEN, background = 'black', cursor = 'dot')
pointSpace.grid(row = 0, column = 0, columnspan = 3, padx = (BORDER_XL, 5), pady = (BORDER_YL, 5))
pointSpace.bind("<Button-2>",  clearPointSpace)

updatePointSpace()

typeSpace = Frame(base)
typeSpace.grid(row = 0, column = 3, rowspan = 2, pady = (5, 5))
chooseEu  = Radiobutton(typeSpace, text = "Euclidean", variable = distType, value = 1, command = bindButtons)
chooseEu.pack(anchor = W)
chooseMh  = Radiobutton(typeSpace, text = "Manhattan", variable = distType, value = 2, command = bindButtons)
chooseMh.pack(anchor = E)

def clear_placeholder(event, e):
    inVal =  e.get()
    if not isinstance(inVal, int):
        e.delete(0, END)

def add_placeholder(event, e, ph):
    inVal = e.get()
    try:
        inVal = int(inVal)
        e.delete(0, END)
        e.insert(0, inVal)
    except Exception:
        e.delete(0, END)
        e.insert(0, ph)        

labelSpace = Frame(base)
labelSpace.grid(row = 1, column = 0, columnspan = 2, padx = 25)
FNumL = Entry (labelSpace, bg = 'white', bd = 3, width = 12)
FNumP = Entry (labelSpace, bg = 'white', bd = 3, width = 12)
FKSet = Entry (labelSpace, bg = 'white', bd = 3, width = 7)
UpdtB = Button(labelSpace, bg = '#9999FF', activebackground = '#444499', bd = 3, text = "Update", padx = 3)
FNumL.insert(0, "Num of Labels")
FNumP.insert(0, "Num of Points")
FKSet.insert(0, "k-level")
FNumL.pack(side = LEFT)
FNumP.pack(side = LEFT)
FKSet.pack(side = LEFT)
UpdtB.pack(side = LEFT)
FNumL.bind("<FocusIn>",  lambda event: clear_placeholder(event, FNumL))
FNumP.bind("<FocusIn>",  lambda event: clear_placeholder(event, FNumP))
FKSet.bind("<FocusIn>",  lambda event: clear_placeholder(event, FKSet))
FNumL.bind("<FocusOut>", lambda event: add_placeholder(event, FNumL, "Num of Labels"))
FNumP.bind("<FocusOut>", lambda event: add_placeholder(event, FNumP, "Num of Points"))
FKSet.bind("<FocusOut>", lambda event: add_placeholder(event, FKSet, "k-level"))
FNumL.bind("<Return>",   updateInput)
UpdtB.bind("<Button-1>", updateInput)

base.mainloop()