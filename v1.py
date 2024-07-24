import tkinter as tk
from tkinter import filedialog, simpledialog
import os

class Whiteboard:
    def __init__(self, root, points=None):
        self.root = root
        self.root.title("Whiteboard")
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.points = points if points else []

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.add_point)

        if self.points:
            self.draw_existing_points()

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)
        self.add_point(event)  # Add point coordinates while dragging

    def add_point(self, event):
        self.points.append((event.x, event.y))

    def get_points(self):
        return self.points

    def draw_existing_points(self):
        for point in self.points:
            x, y = point
            self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black", width=5)

    def save_points_to_file(self, filename):
        with open(filename, 'w') as f:
            for point in self.points:
                f.write(f"{point}\n")

def load_points_from_file(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = line.strip().strip('()').split(',')
            points.append((int(x), int(y)))
    return points

def main():
    root = tk.Tk()
    points = None

    # Ask if user wants to upload an existing file
    upload_file = tk.messagebox.askyesno("Upload File", "Do you want to upload an existing text file with points?")
    
    if upload_file:
        file_path = filedialog.askopenfilename(title="Select file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            points = load_points_from_file(file_path)
        else:
            tk.messagebox.showinfo("No file selected", "No file was selected. Starting with an empty whiteboard.")
    
    whiteboard = Whiteboard(root, points)
    
    root.mainloop()

    # Ask for the filename to save the points
    save_file_name = simpledialog.askstring("Save File", "Enter the name of the file to save the points:", initialvalue="points_output.txt")
    
    if save_file_name:
        whiteboard.save_points_to_file(save_file_name)
        print(f"Points saved to {save_file_name}")
    else:
        print("No file name provided. Points not saved.")

if __name__ == "__main__":
    main()
