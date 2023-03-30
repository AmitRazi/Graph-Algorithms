import tkinter as tk
import Graph


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_window()
        self.canvas = None
        self.active_action = "Add Node"
        self.position_window()
        self.create_widgets()
        self.graph = Graph.Graph()
        self.circles = []

    def create_window(self):
        self.geometry("780x700")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def position_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (400 / 2))
        y_coordinate = int((screen_height / 2) - (200 / 2))
        self.geometry(f"+{x_coordinate}+{y_coordinate}")

    def create_widgets(self):
        self.create_canvas()
        self.create_buttons()

    def create_canvas(self):
        self.canvas = tk.Canvas(self, bg="white", bd=5, relief='groove', width=500, height=500)
        self.canvas.grid(column=0, row=0, sticky='nsew')
        self.canvas.bind('<Button-1>', self.handle_click)

    def create_buttons(self):
        buttons_frame = tk.Frame(self, padx=5, pady=5, relief='sunken')
        buttons_frame.grid(column=0, row=1, columnspan=2)

        add_node_button = tk.Button(buttons_frame, text="Add Node", command=self.handle_inode_button)
        add_node_button.grid(column=0, row=0)

        add_edge_button = tk.Button(buttons_frame, text="Add Edge", command=self.handle_iedge_button)
        add_edge_button.grid(column=1, row=0, padx=5)

        delete_node_button = tk.Button(buttons_frame, text="Delete Node", command=self.handle_dnode_button)
        delete_node_button.grid(column=2, row=0)

        clear_button = tk.Button(buttons_frame, text="Clear", command=self.handle_clear_button)
        clear_button.grid(column=3, row=0, padx=5)

    def draw_node(self, event):
        x = event.x
        y = event.y
        circle_id = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,outline='black',width=2, fill='white')
        return circle_id

    def handle_inode_button(self):
        self.active_action = "Add Node"

    def handle_iedge_button(self):
        self.active_action = "Add Edge"

    def handle_dnode_button(self):
        self.active_action = "Delete Node"

    def handle_dedge_button(self):
        self.active_action = "Delete Edge"

    def handle_clear_button(self):
        self.active_action = "Clear"

    def handle_click(self, event):
        if self.active_action == "Add Node":
            circle_id = self.draw_node(event)
            self.graph.add_node(circle_id,event.x,event.y)

        elif self.active_action == "Delete Node":
            id_to_delete = self.graph.find_node_in_radius(event.x,event.y)
            if id_to_delete >= 0:
                self.canvas.delete(id_to_delete)
                self.canvas.update_idletasks()



window = Window()
window.mainloop()
