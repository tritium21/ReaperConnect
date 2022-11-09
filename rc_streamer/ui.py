import asyncio
import logging
import functools
import tkinter as tk
import tkinter.scrolledtext as scrolledtext


EXIT = False


class TextHandler(logging.Handler):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        self.text.configure(state='normal')
        self.text.insert(tk.END, msg + '\n')
        self.text.configure(state='disabled')
        self.text.yview(tk.END)


class MainUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root = parent
        self.build_gui()

    def build_gui(self):
        self.root.title('ReaperConnect - Streamer Screen')
        self.grid(column=0, row=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Add text widget to display logging info
        st = scrolledtext.ScrolledText(self, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=0, sticky='news')

        # Create textLogger
        self._handler = text_handler = TextHandler(st)

        self._logger = logger = logging.getLogger()
        logger.addHandler(text_handler)


def on_closing(ui):
    global EXIT
    EXIT = True
    ui._logger.removeHandler(ui._handler)


async def tk_app():
    root = tk.Tk()
    root.report_callback_exception = None
    ui = MainUI(root)
    root.protocol("WM_DELETE_WINDOW", functools.partial(on_closing, ui))
    while not EXIT:
        root.update()
        await asyncio.sleep(1.0/20)
    root.destroy()
    raise KeyboardInterrupt
