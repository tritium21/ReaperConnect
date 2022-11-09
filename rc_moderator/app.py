import pathlib
import threading
import tkinter
import tkinter.ttk

import requests

import rc_common.config
import rc_common.crypt


def make_ui(root, config):
    def do(*args):
        message = message_var.get()
        message_var.set('')
        textbox.focus()
        th = threading.Thread(
            target=requests.post,
            args=[
                config['url'],
                {'body': config['encoder'](message)}
            ],
            kwargs={
                'timeout': 10,
            },
        )
        th.start()

    root.title('ReaperConnect - Moderater Screen')
    root.bind('<Return>', do)
    root.bind("<FocusIn>", lambda *x: textbox.focus())
    root.resizable(True, False)
    root.attributes('-topmost', True)

    mainframe = tkinter.ttk.Frame(root, padding='4 4 4 4')
    mainframe.grid(column=0, row=0, sticky='NEWS')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=0)
    mainframe.rowconfigure(0, weight=0)

    message_var = tkinter.StringVar()
    textbox = tkinter.ttk.Entry(mainframe, width=100, textvariable=message_var)
    textbox.grid(column=0, row=0, sticky='NEWS')
    tkinter.ttk.Button(mainframe, text="Send", command=do).grid(column=1, row=0, sticky='NEWS')
    textbox.focus()


def get_config(conf_path):
    conf_path = pathlib.Path(conf_path).resolve()
    config = rc_common.config.load(conf_path)
    key = config.key
    encrypt = rc_common.crypt.from_key(key).encrypt
    return {'url': config.url, 'encoder': encrypt}


def main(conf_path):
    root = tkinter.Tk()
    make_ui(root, get_config(conf_path))
    root.mainloop()
