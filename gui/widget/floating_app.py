# from gui import OverlayWindow
import json
import time
import tkinter as tk
from tkinter import ttk

from gui import ComponentOverlay


class FloatingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__components = Components()
        self.__overlay = ComponentOverlay()

        # coordinates app right now
        self.cord = {
            "x": 0,
            "y": 0
        }

        # Canvas to create a rectangle   
        self.canvas = self.create_canvas()
        self.canvas.pack(fill=tk.BOTH, expand=True)

        
        self.__components.create_frame(self)
        # self.canvas.lift()
        self.setup_widget()
        self.setup_canvas()
        
        # self.__overlay.mainloop()

    """
    """
    def create_canvas(self) -> tk.Canvas:
        canvas = tk.Canvas(master=self,
                           bg="white",
                           highlightthickness=0)
        return canvas

    """
    """
    def setup_canvas(self) -> None:
        self.canvas.create_rectangle((50, 50, 100, 75),
                                fill="red",
                                outline="grey",
                                tags="overlay")
        
        self.canvas.create_rectangle((50, 75, 100, 100),
                                fill="blue",
                                outline="grey",
                                tags="delete")
        

        self.canvas.tag_bind("overlay", "<ButtonPress-1>", self.start_drag)
        
        self.canvas.tag_bind("overlay", "<ButtonPress-2>", self.start_ocr)
        self.canvas.tag_bind("overlay", "<ButtonPress-3>", self.stop_ocr)
        
        self.canvas.tag_bind("overlay", "<B1-Motion>", self.do_drag)

    """
    """
    def setup_widget(self):
        # window fullscreen
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight() - 1}+0+0")

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "white")

        self.configure(bg="white")
        
    """
    """
    def start_drag(self, event):
        self.cord["x"] = event.x
        self.cord["y"] = event.y
        
        print("abc")
        
    def start_ocr(self,event):
        print("abc2")
        self.__overlay.start()
        # self.__overlay.destroy()
        
    def stop_ocr(self, event):
        # 
        
        self.__overlay.frame.destroy()

    
    """
    """
    def do_drag(self, event):
        dx = event.x - self.cord["x"]
        dy = event.y - self.cord["y"]

        self.canvas.move("overlay", dx, dy)
        self.canvas.move("delete", dx, dy)
        
        self.cord["x"] = event.x
        self.cord["y"] = event.y




class Components():
    def __init__(self):
           # super().__init__(parent)
        self.__frame: ttk.Frame | None = None
        self.__data: list[dict] | None = None
        
    """
    """
    def get_frame(self) -> tk.Frame | None:
        if self.__frame is not None:
            return self.__frame
        else:
            return None

    """
    """
    def create_frame(self, parent) -> None :
        if self.__frame is not None:
            self.__frame.destroy()
            self.__frame = None
            
        self.__frame = tk.Frame(master=parent, background="white", width=1920, height=1080 - 1)
        self.__frame.bind("<Escape>", lambda e: self.__frame.pack_forget())
        self.draw_text()
        
        self.__frame.place(x=0, y=0, anchor="nw")
        # self.__frame.lower()
        
        
    """
    """
    def draw_text(self) -> None :
        with open("translate\\result.json", "r") as f:
            self.__data = json.load(f)
        
        for item in self.__data:
            text  = item["LineText"]
            x1,y1,x2,y2 = item["BoundingBox"]
            
            label  = tk.Label(master=self.__frame,
                              text=text,
                              bg="grey",
                              font="Calibri 13 bold")
            
            label.place(x=x1, y=y1, anchor="nw")
            
        


if __name__ == "__main__":
    app = FloatingApp()
    app.mainloop()