
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox
from rivescript import RiveScript
import time


class CHATBOT:

    def __init__(self):
        self.rs = RiveScript()

    def start_chatbot(self, path):
        self.rs.load_directory(path)
        self.rs.sort_replies()

    def get_reply(self, message):
        return self.rs.reply("localuser", message).encode('utf-8')


class GUI:

    def __init__(self, master, path):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_gui()
        self.chatbot = CHATBOT()
        self.chatbot.start_chatbot(path)

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box:', font=(
            "Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(
            frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(
            frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=(
            "Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(
            frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_enter_key_pressed(self, event):
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = data.encode('utf-8')

        reply_chatbot = self.chatbot.get_reply(data)

        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)

        self.chat_transcript_area.insert(
            'end', reply_chatbot.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)

        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)


if __name__ == '__main__':
    root = Tk()
    gui = GUI(master=root, path="./brain")
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
