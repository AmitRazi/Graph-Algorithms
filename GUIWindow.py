import tkinter as tk
import Graph
from GraphEdge import Edge
from typing import List, Set
import GraphAlgorithms


class Window(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.create_window(title)  # Create the window with the given title
        # Define various variables and attributes needed for the window
        self.canvas = None
        self.zoom_center = None
        self.zoom_factor = 1.0
        self.scale_factor = 1.0
        self.active_action = "Add Node"  # Default action
        self.delay_entry = None  # For user input of delay
        self.algorithm = title  # Algorithm to use, determined by window title
        self.position_window()  # Set the window position
        self.create_widgets()  # Create the buttons, text box, etc
        self.source_node = None
        self.output_text = self.create_output_text()  # Output text box
        self.graph = Graph.Graph(self)  # Initialize a Graph object
        self.graph_algos = GraphAlgorithms.GAlgorithm(self.graph)  # Graph algorithms object
        self.highlighted_node = None  # The node that is currently highlighted
        self.source_node_circle_id = None

    def create_window(self, title):
        self.geometry("780x700")
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def create_output_text(self):
        output_text = tk.Text(self, wrap=tk.WORD, height=10, padx=5, pady=5, relief='sunken')
        output_text.grid(column=0, row=2, sticky='nsew')
        output_text.insert(tk.END, "Messages:\n")
        output_text.config(state=tk.DISABLED)
        return output_text

    def print_to_gui(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

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
        self.canvas.bind('<Button-1>', self.handle_chosen_action)
        self.canvas.bind('<Motion>', self.handle_motion)
        self.canvas.bind("<MouseWheel>", self.zoom)

    def create_buttons(self):
        buttons_frame = tk.Frame(self, padx=5, pady=5, relief='sunken')  # Create a frame to hold the buttons
        buttons_frame.grid(column=0, row=1, columnspan=2, sticky='w')

        algo_button_frame = tk.Frame(self, padx=5, pady=5, relief='sunken')  # Create a frame for algorithm buttons
        algo_button_frame.grid(column=0, row=1, columnspan=2, sticky='e')

        # Check which algorithm to use and create the corresponding "play" button
        if self.algorithm == 'Brooks Algorithm':
            play_button = tk.Button(algo_button_frame, text="▶", font=('Arial', 12),
                                    command=self.run_brooks_algorithm)
            play_button.grid(column=0, row=0, padx=2, pady=5, sticky='w')
        else:
            play_button = tk.Button(algo_button_frame, text="▶", font=('Arial', 12),
                                    command=self.run_hungarian_algorithm)
            play_button.grid(column=0, row=0, padx=2, pady=5, sticky='w')

        # Create an entry field for delay input
        self.delay_entry = tk.Entry(algo_button_frame, font=('Arial', 12), bd=2, relief='groove', width=15)
        self.delay_entry.insert(0, "Delay in seconds:")
        self.delay_entry.bind("<Button-1>", self.handle_entry_click)
        self.delay_entry.grid(column=1, row=0, padx=2, pady=5, sticky='w')

        # Create various buttons for different actions
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

    def run_brooks_algorithm(self):
        delay = int(self.delay_entry.get())
        self.graph_algos.brooks_algorithm(self.graph,delay)

    def draw_node(self, event):
        x = event.x
        y = event.y

        circle_id = self.canvas.create_oval(x - 20 * self.scale_factor, y - 20 * self.scale_factor,
                                            x + 20 * self.scale_factor, y + 20 * self.scale_factor, outline='black',
                                            width=2, fill='white')

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

    def handle_motion(self, event):
        # if no source node is selected
        if self.source_node_circle_id is None:
            # Find the node under the mouse cursor
            node_circle_id = self.graph.find_node_in_radius(event.x, event.y)

            # if the mouse cursor is over a node
            if node_circle_id >= 0:
                # if the node under the mouse is not the currently highlighted node
                if self.highlighted_node != node_circle_id:
                    # if there is a node currently highlighted
                    if self.highlighted_node is not None:
                        # change the color of the currently highlighted node back to white
                        self.canvas.itemconfigure(self.highlighted_node, fill='white')

                    # change the color of the new node to red to highlight it
                    self.canvas.itemconfigure(node_circle_id, fill='red')
                    # update the currently highlighted node
                    self.highlighted_node = node_circle_id
            else:
                # if the mouse cursor is not over a node and there is a currently highlighted node
                if self.highlighted_node is not None:
                    # change the color of the currently highlighted node back to white
                    self.canvas.itemconfigure(self.highlighted_node, fill='white')
                    # remove the reference to the highlighted node since there is none now
                    self.highlighted_node = None

    def draw_edge(self, dest_id):
        source_x, source_y = self.graph.find_node_by_id_coords(self.source_node)
        dest_x, dest_y = self.graph.find_node_by_id_coords(dest_id)

        return self.canvas.create_line(source_x, source_y, dest_x, dest_y, fill='black', width=2)

    def color_edge(self, edge_id, color: str):
        self.canvas.itemconfigure(edge_id, fill=color)
        self.canvas.update()

    def color_node(self, node_id, color: str):
        self.canvas.itemconfigure(node_id, fill=color)
        self.canvas.update()

    def color_node_outline(self,node_id,color:str):
        self.canvas.itemconfigure(node_id, outline=color, width=2)

    def direct_graph(self, matching: Set[Edge], edge_list: List[Edge]):
        for edge in edge_list:
            coords = self.canvas.coords(edge.id)

            if edge.source.x == coords[0]:
                self.canvas.itemconfigure(edge.id, arrow=tk.LAST)
            else:
                self.canvas.itemconfigure(edge.id, arrow=tk.FIRST)

    def handle_chosen_action(self, event):
        # If the chosen action is to "Add Node"
        if self.active_action == "Add Node":
            # Find the node under the mouse cursor
            node_circle_id = self.graph.find_node_in_radius(event.x, event.y)
            # If there isn't already a node where the user clicked (indicated by node_circle_id < 0)
            if node_circle_id < 0:
                # Draw the node at the event (click) location
                circle_id = self.draw_node(event)
                # Add the newly drawn node to the graph
                self.graph.add_node(circle_id, event.x, event.y, self.scale_factor)

        # If the chosen action is to "Delete Node"
        elif self.active_action == "Delete Node":
            # Find the node under the mouse cursor
            id_to_delete = self.graph.find_node_in_radius(event.x, event.y)
            # If there is a node where the user clicked
            if id_to_delete >= 0:
                # Delete the node from the canvas
                self.canvas.delete(id_to_delete)
                # Delete the node from the graph, and get the list of associated edges
                edge_list = self.graph.delete_node(id_to_delete)
                print("Deleted " + str(len(edge_list)) + " edges.")
                # Delete all associated edges from the canvas
                for edge in edge_list:
                    self.canvas.delete(edge)

        # If the chosen action is to "Add Edge"
        elif self.active_action == "Add Edge":
            # Find the node under the mouse cursor
            node_circle_id = self.graph.find_node_in_radius(event.x, event.y)
            # If there is a node where the user clicked
            if node_circle_id >= 0:
                # If no source node has been selected yet
                if self.source_node is None:
                    # Set the clicked node as the source node
                    self.source_node = node_circle_id
                    self.source_node_circle_id = node_circle_id
                    # Highlight the source node in red
                    self.canvas.itemconfigure(self.source_node_circle_id, fill='red')
                else:
                    # Draw an edge from the source node to the clicked node
                    edge_id = self.draw_edge(node_circle_id)
                    # Add the new edge to the graph
                    self.graph.add_edge(self.source_node, node_circle_id, edge_id)
                    # Remove the highlight from the source node
                    self.canvas.itemconfigure(self.source_node_circle_id, fill='white')
                    # Reset the source node as none
                    self.source_node = None
                    self.source_node_circle_id = None

class LauncherWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algorithm Launcher")
        self.create_buttons()
        self.position_window()

    def position_window(self):
        window_width = 200
        window_height = 100

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"+{x_coordinate}+{y_coordinate}")

    def create_buttons(self):
        hungarian_button = tk.Button(self, text="Hungarian Algorithm", command=self.open_hungarian_window)
        hungarian_button.pack(padx=20, pady=10)

        brooks_button = tk.Button(self, text="Brooks Algorithm", command=self.open_brooks_window)
        brooks_button.pack(padx=20, pady=10)

    def open_hungarian_window(self):
        self.destroy()
        window = Window("Hungarian Algorithm")
        window.mainloop()

    def open_brooks_window(self):
        self.destroy()
        brooks_window = Window("Brooks Algorithm")
        brooks_window.mainloop()


launcher_window = LauncherWindow()
launcher_window.mainloop()
