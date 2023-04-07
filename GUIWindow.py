import tkinter as tk
import Graph
from GraphEdge import Edge
from typing import List, Set
from GraphAlgorithms import GAlgorithm


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_window()
        self.canvas = None
        self.zoom_center = None
        self.zoom_factor = 1.0
        self.scale_factor = 1.0

        self.active_action = "Add Node"
        self.delay_entry = None
        self.position_window()
        self.create_widgets()
        self.source_node = None
        self.output_text = self.create_output_text()
        self.graph = Graph.Graph(self)
        self.graph_algos = GAlgorithm(self.graph)
        self.highlighted_node = None
        self.source_node_circle_id = None

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
        self.canvas.bind('<Button-1>', self.handle_choosen_action)
        self.canvas.bind('<Motion>', self.handle_motion)

        x_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        x_scrollbar.grid(column=0, row=1, sticky='ew')
        y_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        y_scrollbar.grid(column=1, row=0, sticky='ns')

        self.canvas.config(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        x_scrollbar.config(command=self.canvas.xview)
        y_scrollbar.config(command=self.canvas.yview)

        self.canvas.bind("<MouseWheel>", self.zoom)

    def create_buttons(self):
        buttons_frame = tk.Frame(self, padx=5, pady=5, relief='sunken')
        buttons_frame.grid(column=0, row=1, columnspan=2, sticky='w')

        algo_button_frame = tk.Frame(self, padx=5, pady=5, relief='sunken')
        algo_button_frame.grid(column=0, row=1, columnspan=2, sticky='e')

        bipartite_button = tk.Button(algo_button_frame, text="▶", font=('Arial', 12),
                                     command=self.run_hungarian_algorithm)
        bipartite_button.grid(column=0, row=0, padx=2, pady=5, sticky='w')

        self.delay_entry = tk.Entry(algo_button_frame, font=('Arial', 12), bd=2, relief='groove', width=15)
        self.delay_entry.insert(0, "Delay in seconds:")
        self.delay_entry.bind("<Button-1>", self.handle_entry_click)
        self.delay_entry.grid(column=1, row=0, padx=2, pady=5, sticky='w')

        add_node_button = tk.Button(buttons_frame, text="Add Node", padx=5, pady=5, command=self.handle_inode_button)
        add_node_button.grid(column=0, row=0, padx=5)

        add_edge_button = tk.Button(buttons_frame, text="Add Edge", padx=5, pady=5, command=self.handle_iedge_button)
        add_edge_button.grid(column=1, row=0, padx=5)

        delete_node_button = tk.Button(buttons_frame, text="Delete Node", padx=5, pady=5,
                                       command=self.handle_dnode_button)
        delete_node_button.grid(column=2, row=0, padx=5)

        print_graph_button = tk.Button(buttons_frame, text="Print Graph", padx=5, pady=5,
                                       command=self.handle_pgraph_button)
        print_graph_button.grid(column=3, row=0, padx=5)

        clear_button = tk.Button(buttons_frame, text="Clear", padx=5, pady=5, command=self.handle_clear_button)
        clear_button.grid(column=4, row=0, padx=5)

    def zoom(self, event):
        self.scale_factor *= 1.1 if event.delta > 0 else 0.9
        self.zoom_factor = 1.1 if event.delta > 0 else 0.9
        self.zoom_center = event.x, event.y

        for node in self.graph.node_list:
            node.x = (node.x - self.zoom_center[0]) * self.zoom_factor + self.zoom_center[0]
            node.y = (node.y - self.zoom_center[1]) * self.zoom_factor + self.zoom_center[1]
            node._radius *= self.zoom_factor

        self.canvas.scale("all", event.x, event.y, self.zoom_factor, self.zoom_factor)

    def run_hungarian_algorithm(self):
        delay = int(self.delay_entry.get())
        is_bipartite = self.graph_algos.hungarian_algorithm(delay)
        print(is_bipartite)
        self.print_to_gui(f"Bipartite: {is_bipartite}")

    def draw_node(self, event):
        x = event.x
        y = event.y

        circle_id = self.canvas.create_oval(x - 20*self.scale_factor, y - 20*self.scale_factor, x + 20*self.scale_factor, y + 20*self.scale_factor, outline='black', width=2, fill='white')
        
        return circle_id

    def handle_inode_button(self):
        self.active_action = "Add Node"

    def handle_iedge_button(self):
        self.active_action = "Add Edge"

    def handle_dnode_button(self):
        self.active_action = "Delete Node"

    def handle_dedge_button(self):
        self.active_action = "Delete Edge"

    def handle_entry_click(self, event):
        self.delay_entry.delete(0, tk.END)

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

    def handle_motion(self, event):
        if self.source_node_circle_id is None:
            node_circle_id = self.graph.find_node_in_radius(event.x, event.y)

            if node_circle_id >= 0:
                if self.highlighted_node != node_circle_id:
                    if self.highlighted_node is not None:
                        self.canvas.itemconfigure(self.highlighted_node, fill='white')

                    self.canvas.itemconfigure(node_circle_id, fill='red')
                    self.highlighted_node = node_circle_id
            else:
                if self.highlighted_node is not None:
                    self.canvas.itemconfigure(self.highlighted_node, fill='white')
                    self.highlighted_node = None

    def draw_edge(self, dest_id):
        source_x, source_y = self.graph.find_node_by_id(self.source_node)
        dest_x, dest_y = self.graph.find_node_by_id(dest_id)

        return self.canvas.create_line(source_x, source_y, dest_x, dest_y, fill='black', width=2)

    def color_edge(self, edge_id, color: str):
        self.canvas.itemconfigure(edge_id, fill=color)
        self.canvas.update()

    def direct_graph(self, matching: Set[Edge], edge_list: List[Edge]):
        for edge in edge_list:
            coords = self.canvas.coords(edge.id)

            if edge.source.x == coords[0]:
                self.canvas.itemconfigure(edge.id, arrow=tk.LAST)
            else:
                self.canvas.itemconfigure(edge.id, arrow=tk.FIRST)

    def handle_choosen_action(self, event):
        if self.active_action == "Add Node":
            circle_id = self.draw_node(event)
            self.graph.add_node(circle_id, event.x, event.y, self.scale_factor)

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
                    self.source_node_circle_id = node_circle_id
                    self.canvas.itemconfigure(self.source_node_circle_id, fill='red')
                else:
                    edge_id = self.draw_edge(node_circle_id)
                    self.graph.add_edge(self.source_node, node_circle_id, edge_id)
                    self.canvas.itemconfigure(self.source_node_circle_id, fill='white')
                    self.source_node = None
                    self.source_node_circle_id = None


window = Window()
window.mainloop()
