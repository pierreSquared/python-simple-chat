"""
demonstracja ukladacza grid
"""
import tkinter as tk


class View:
    def __init__(self, root, send_queue, receive_queue):
        self.root = root
        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.root.title("Moja aplikacja")
        self.root.minsize(600, 400)
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.chat_window = tk.Text(self.mainFrame, state=tk.DISABLED)
        self.chat_window.grid(column=0, row=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.users = tk.Listbox(self.mainFrame )
        self.users.grid(column=1, row=0, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.users.insert(tk.END, "ALL")
        self.users.select_set(0)
        self.users.event_generate("<<ListboxSelect>>")
        self.users.insert(tk.END, "OTHER")
        self.users.insert(tk.END, "TEST")

        self.input_text = tk.StringVar()
        self.input = tk.Entry(self.mainFrame, textvariable=self.input_text)
        self.input.grid(column=0, row=1, sticky=tk.N + tk.S + tk.W + tk.E)
        self.input.bind("<Return>", self.on_send_pressed)

        self.sendButton = tk.Button(self.mainFrame, text="Send")
        self.sendButton.grid(column=0, row=2, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.sendButton.bind("<Button-1>", self.on_send_pressed)

        self.mainFrame.rowconfigure(0, weight=4)
        self.mainFrame.rowconfigure(1, weight=2)
        self.mainFrame.rowconfigure(2, weight=1)

        self.mainFrame.columnconfigure(0, weight=3)
        self.mainFrame.columnconfigure(1, weight=1)

    def main_loop(self):
        self.root.mainloop()

    def start_update_loop(self):
        self.root.after(50, self.update_loop)

    def update_loop(self):
        if not self.receive_queue.empty():
            print("Updating chat window")
            msg, sender, receiver = self.receive_queue.get()
            self.chat_window.config(state=tk.NORMAL)
            self.chat_window.insert(tk.END, sender + "->" + receiver + ": " + msg + "\n")
            self.chat_window.config(state=tk.DISABLED)
        self.root.after(50, self.update_loop)

    def on_send_pressed(self, event):
        self.send_queue.put((self.input_text.get(), self.users.get(self.users.curselection()[0])))
        self.input_text.set("")


def create_view(send_queue, receive_queue):
    root = tk.Tk()
    app = View(root, send_queue, receive_queue)
    return app