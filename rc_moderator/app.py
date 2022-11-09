import base64
import pathlib
import tkinter as tk
from tkinter import ttk

from requests import post
import tomlkit
import nacl.secret


def make_ui(root, config):
    def do(*args):
        message = message_var.get()
        message_var.set('')
        textbox.focus()
        post(config['url'], {'body': config['encoder'](message)})

    root.title('ReaperConnect - Moderater Screen')
    root.bind('<Return>', do)
    root.bind("<FocusIn>", lambda *x: textbox.focus())
    root.resizable(True, False)
    root.attributes('-topmost', True)

    mainframe = ttk.Frame(root, padding='4 4 4 4')
    mainframe.grid(column=0, row=0, sticky='NEWS')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=0)
    mainframe.rowconfigure(0, weight=0)

    message_var = tk.StringVar()
    textbox = ttk.Entry(mainframe, width=100, textvariable=message_var)
    textbox.grid(column=0, row=0, sticky='NEWS')
    ttk.Button(mainframe, text="Send", command=do).grid(column=1, row=0, sticky='NEWS')
    textbox.focus()


def get_config(conf_path):
    conf_path = pathlib.Path(conf_path).resolve()
    conf = {
        'encoder': (lambda x: x),
        'url': 'http://localhost:42069/say'
    }
    if not conf_path.exists():
        return conf
    data = tomlkit.loads(conf_path.read_text(encoding='utf-8'))
    conf['url'] = data.get('url', conf['url'])
    key = data.get('key')
    if key is not None:
        key = base64.b64decode(key)
        box = nacl.secret.SecretBox(key)

        def inner(message):
            cyphertext = box.encrypt(message.encode('utf-8'))
            return base64.b64encode(cyphertext)
    conf['encoder'] = inner
    return conf


def main(conf_path):
    root = tk.Tk()
    make_ui(root, get_config(conf_path))
    root.mainloop()
