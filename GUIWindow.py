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
        self.circles = []
        self.source_node = None
        self.output_text = self.create_output_text()
        self.graph = Graph.Graph(self)

    def create_window(self):
        self.geometry("780x700")
        self.title("Hungarian Method")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def create_output_text(self):  # New function
        output_text = tk.Text(self, wrap=tk.WORD, height=10, padx=5, pady=5, relief='sunken')
        output_text.grid(column=0, row=2, sticky='nsew')
        output_text.insert(tk.END, "Messages:\n")
        output_text.config(state=tk.DISABLED)  # Make the text widget read-only
        return output_text

    def print_to_gui(self, message):
        self.output_text.config(state=tk.NORMAL)  # Enable editing
        self.output_text.insert(tk.END, message + "\n")  # Append the message
        self.output_text.config(state=tk.DISABLED)  # Disable editing
        self.output_text.see(tk.END)  # Scroll to the end

    def position_window(self):
        window_width = 780
        window_height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"+{x_coordinate}+{y_coordinate}")

    def create_widgets(self):
        self.create_canvas()
        self.create_buttons()
        self.create_output_text()

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

        print_graph_button = tk.Button(buttons_frame, text="Print Graph", command=self.handle_pgraph_button)
        print_graph_button.grid(column=3, row=0)

        clear_button = tk.Button(buttons_frame, text="Clear", command=self.handle_clear_button)
        clear_button.grid(column=4, row=0, padx=5)

    def draw_node(self, event):
        x = event.x
        y = event.y
        circle_id = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline='black', width=2, fill='white')
        return circle_id

    def handle_inode_button(self):
        self.active_action = "Add Node"

    def handle_iedge_button(self):
        self.active_action = "Add Edge"

    def handle_dnode_button(self):
        self.active_action = "Delete Node"

    def handle_dedge_button(self):
        self.active_action = "Delete Edge"

    def clear_message_box(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(2.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

    def handle_pgraph_button(self):
        self.clear_message_box()
        self.print_to_gui("\nV(G):")
        for node in self.graph.node_list:
            self.print_to_gui(node.__str__())
        self.print_to_gui("E(G):")
        for edge in self.graph.edge_list:
            self.print_to_gui(edge.__str__())

    def handle_clear_button(self):
        self.graph.delete_graph()
        print("Deleted graph.")

    def draw_edge(self, dest_id):
        source_x, source_y = self.graph.find_node_by_id(self.source_node)
        dest_x, dest_y = self.graph.find_node_by_id(dest_id)
        return self.canvas.create_line(source_x, source_y, dest_x, dest_y, fill='black', width=2)

    def handle_click(self, event):
        if self.active_action == "Add Node":
            circle_id = self.draw_node(event)
            self.graph.add_node(circle_id, event.x, event.y)

        elif self.active_action == "Delete Node":
            id_to_delete = self.graph.find_node_in_radius(event.x, event.y)
            if id_to_delete >= 0:
                self.canvas.delete(id_to_delete)
                edge_list = self.graph.delete_node(id_to_delete)
                print("Deleted " + str(len(edge_list)) + " edges.")
                for edge in edge_list:
                    self.canvas.delete(edge)

        elif self.active_action == "Add Edge":
            node_circle_id = self.graph.find_node_in_radius(event.x, event.y)
            if node_circle_id >= 0:
                if self.source_node is None:
                    self.source_node = node_circle_id
                else:
                    edge_id = self.draw_edge(node_circle_id)
                    self.graph.add_edge(self.source_node, node_circle_id, edge_id)
                    self.source_node = None


window = Window()
window.mainloop()
