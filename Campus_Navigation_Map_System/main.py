import os
import heapq
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from parser import ParseFile
from math import sqrt


class Marker():
    def __init__(self, coords, name=None, color="Red"):
        self.coords = coords
        self.name = name
        self.color = color


class LocationMarker(Marker):
    def __init__(self, coords, name=None, color="blue"):
        super().__init__(coords, name, color)


class PathMarker(Marker):
    def __init__(self, coords, name=None, color="red"):
        super().__init__(coords, name, color)


def CloseWindow(event=None):
    root.destroy()


def DrawMarkers(markers, canvas):
    if isinstance(markers, list):
        for marker in markers:
            if isinstance(marker, list):
                for i in marker:
                    x, y = i.coords
                    canvas.create_rectangle(x, y, x + 5, y + 5, fill=i.color)
            else:
                x, y = marker.coords
                canvas.create_rectangle(x, y, x + 5, y + 5, fill=marker.color)
    else:
        x, y = markers.coords
        canvas.create_rectangle(x, y, x + 5, y + 5, fill=markers.color)


def CreateMap(root, canvasBackground):
    canvas = tk.Canvas(right, bg=canvasBackground, highlightthickness=0)

    # Add scrollbars
    scroll_x = ttk.Scrollbar(right, orient="horizontal", command=canvas.xview)
    scroll_y = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
    canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    scroll_x.pack(side="bottom", fill="x")
    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    return canvas


def GetMarkersFromFile(file):
    locationMarkers = []
    pathMarkers = []

    locationMarkerCoords, locationMarkersNames, pathMarkerCoords = ParseFile(file)

    for i in range(len(locationMarkerCoords)):
        locationMarkers.append(LocationMarker(locationMarkerCoords[i], name=locationMarkersNames[i]))

    for i in pathMarkerCoords:
        temp = []
        for j in i:
            temp.append(PathMarker(j))
        pathMarkers.append(temp)

    return locationMarkers, pathMarkers


def GetPathLength(graph, start_coords, end_coords):
    to_visit = [(0, start_coords)]
    shortest_distances = {start_coords: 0}
    predecessors = {}

    while to_visit:
        current_dist, current_node = heapq.heappop(to_visit)

        if current_node == end_coords:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = predecessors.get(current_node)
            path.reverse()
            return current_dist, path

        for neighbor, length in graph[current_node].items():
            new_dist = current_dist + length
            if neighbor not in shortest_distances or new_dist < shortest_distances[neighbor]:
                shortest_distances[neighbor] = new_dist
                predecessors[neighbor] = current_node
                heapq.heappush(to_visit, (new_dist, neighbor))

    return None, None


def GetDistance(coords1, coords2):
    x1, y1 = coords1
    x2, y2 = coords2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def BuildGraph(pathMarkerList):
    graph = {}

    for path in pathMarkerList:
        for i in range(len(path) - 1):
            coords1 = path[i].coords
            coords2 = path[i + 1].coords
            distance = round(GetDistance(coords1, coords2), 2)

            if coords1 not in graph:
                graph[coords1] = {}
            if coords2 not in graph:
                graph[coords2] = {}

            graph[coords1][coords2] = distance
            graph[coords2][coords1] = distance

    return graph


def HighlightPath(path):
    map.delete("path")  # Clear previous path first
    for i in range(len(path) - 1):
        map.create_line(
            path[i], path[i + 1], fill="blue", width=3, tags="path")


def GetCoordsFromName(name):
    global locationMarkersList
    for i in locationMarkersList:
        if i.name.strip() == name:
            return i.coords


def UpdateMap(a, b):
    path = []
    distance, path = GetPathLength(graph, GetCoordsFromName(a), GetCoordsFromName(b))
    if path:
        HighlightPath(path)


# Main window setup
root = tk.Tk()
root.title("Campus Navigation System")
root.geometry("1200x800")
root.minsize(1000, 700)

# Paths handling
cwd = os.getcwd()
file = os.path.join(cwd, "coords.txt")
backgroundImagePath = os.path.join(cwd, "map1.png")

# Custom font
cusfont = tkfont.Font(family="Aptos", size=14)

# Main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Configure grid
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Left frame (controls)
left = tk.Frame(main_frame, width=300, bg="black")
left.grid(row=0, column=0, sticky="nswe")

# Right frame (map)
right = tk.Frame(main_frame, bg="white")
right.grid(row=0, column=1, sticky="nsew")

# Create map
map = CreateMap(root, "white")
try:
    backgroundImage = tk.PhotoImage(file=backgroundImagePath)
    map.create_image(0, 0, anchor="nw", image=backgroundImage)
    map.image = backgroundImage  # Keep reference
    map.config(scrollregion=map.bbox("all"))
except Exception as e:
    print(f"Error loading map image: {e}")

# Load markers
locationMarkersList, pathMarkerList = GetMarkersFromFile(file)
graph = BuildGraph(pathMarkerList)


# UI Functions
def dropdown():
    global ask, sel, menu, confirmbutton, placeholder
    global ask0, sel0, menu0, placeholder0

    options = ["B", "C", "Annex", "Library", "Canteen", "Admin", "ATM"]
    sel = tk.StringVar()
    sel0 = tk.StringVar()

    ask0 = ttk.Label(left, text="Select Starting point", font=cusfont, background="black", foreground="white")
    ask0.place(relx=0.5, rely=0.2, anchor="center")
    menu0 = ttk.Combobox(left, values=options, textvariable=sel0, font=cusfont, state="readonly")
    menu0.place(relx=0.5, rely=0.3, anchor="center")
    placeholder0 = ttk.Label(left, text="Pick an option below", font=cusfont, foreground="gray")
    placeholder0.place(relx=0.5, rely=0.3, anchor="center")

    def on_select0(event):
        placeholder0.place_forget()

    menu0.bind("<<ComboboxSelected>>", on_select0)

    ask = ttk.Label(left, text="Select destination", font=cusfont, background="black", foreground="white")
    ask.place(relx=0.5, rely=0.4, anchor="center")
    menu = ttk.Combobox(left, values=options, textvariable=sel, font=cusfont, state="readonly")
    menu.place(relx=0.5, rely=0.5, anchor="center")
    placeholder = ttk.Label(left, text="Pick an option below", font=cusfont, foreground="gray")
    placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def on_select(event):
        placeholder.place_forget()

    menu.bind("<<ComboboxSelected>>", on_select)

    confirmbutton = ttk.Button(left, text="Confirm selection", command=clconfirmbutton)
    confirmbutton.place(relx=0.5, rely=0.6, anchor="center")


def crhomebutton():
    global backbutton
    backbutton = ttk.Button(left, text="Home", command=clbackbutton)
    backbutton.place(relx=0.5, rely=0.9, anchor="center")


def clbackbutton():
    resetui()
    dropdown()
    crhistorrybutton()
    crhomebutton()


def crhistorrybutton():
    global historybutton
    historybutton = ttk.Button(left, text="View history", command=clhistorybutton)
    historybutton.place(relx=0.5, rely=0.7, anchor="center")


def clhistorybutton():
    global log
    resetui()
    try:
        with open("history.txt", "r") as file:
            history = file.read().strip() or "No results"
    except FileNotFoundError:
        history = "No results"

    log = ttk.Label(left, text=history, font=cusfont, background="black", foreground="white")
    log.place(relx=0.5, rely=0.5, anchor="center")

    crclrhistorybutton()
    crhomebutton()


def crclrhistorybutton():
    global clrhistorybutton
    clrhistorybutton = ttk.Button(left, text="Clear history", command=clclrhistorybutton)
    clrhistorybutton.place(relx=0.5, rely=0.7, anchor="center")


def clclrhistorybutton():
    with open("history.txt", "w") as file:
        pass
    log.config(text="History cleared")
    clrhistorybutton.destroy()


def clconfirmbutton():
    global selopt, startopt
    selopt = sel.get()
    startopt = sel0.get()

    if not selopt:
        disp_text = "No option selected for destination"
    elif not startopt:
        disp_text = "No option selected for starting point"
    else:
        disp_text = f"Showing route From {startopt} to {selopt}"
        with open("history.txt", "a") as file:
            file.write(f"{startopt} -> {selopt}\n")

    resetui()

    if not (startopt == "" or selopt == ""):
        UpdateMap(startopt, selopt)

    global disp
    disp = ttk.Label(left, text=disp_text, font=cusfont, background="black", foreground="white")
    disp.place(relx=0.5, rely=0.4, anchor="center")

    crhomebutton()
    crhistorrybutton()


def resetui():
    for widget in left.winfo_children():
        widget.destroy()


def start():
    dropdown()
    crhomebutton()
    crhistorrybutton()


root.bind("<Escape>", CloseWindow)
start()
root.mainloop()