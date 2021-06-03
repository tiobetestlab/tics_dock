#!/usr/bin/env python3

'''
Copytight 2001-2021 TIOBE Software b.v.
# $Id: tics_dock.py 41376 2020-11-05 17:46:52Z wener $
# $URL: svn+ssh://esp.tiobe.com/home/wilde/svnrepository/misc/trunk/tics_dock/tics_dock.py $
'''

from tkinter import Button
from tkinter import Entry
from tkinter import END
from tkinter import Tk
from tkinter import Toplevel
from tkinter import PhotoImage
from tkinter import Label
from tkinter import Menu
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
import ntpath
import os
import subprocess
import sys
import yaml
import re


CFG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/tics_dock.cfg'
TICS_LOGO_RAW = b'R0lGODlhMgAUAOeuAAAjgwAthwwxjAM5jAA7kwY6jQk7jgw8jwBAkgBBkwBClABDlQBFlgRElhY/\nkxdAjgBGlwZFkQdFlwBHmABImQpGkgBKmw1HkwBLnA9IlBJIlQBOmQBPnwJPmhZKlwVPmxhLmAlQ\nnABUngxRnQBVnwBWoA9SngBXogBXoxJTnwBYpCBQlwBZpQNaphdWnABdpwBeqCdUnBtYngBfqQpd\nogBgqh5aoBFfpSBboQBkqQBlqhNgpiJcowBmqyNdpBZhpwJnrBhiqAZorRpjqRxkqgpprgBtsQ5q\nrwBusixjpS1kpi5lpxRssTBmqBZtshVurSRqqhdvrhlutDJoqhtvtRpwryltrRxxsCxurx5ysT9q\npy5vsCBzsjhuqi9wsSJ0syR1tBR6uSV2tj1yrjR2sUN3szp6tTB/uTx8uDKAujOBuz6AtTWCvD+B\ntjaDvUGCt0uBt0SFu06DukaGvEeHvUiJvkmKv0qLwFuJuk2NwlyKvF2LvWCNv2eNuluSw1yTxF2U\nxVaYx1eZyG2UwXOax3ubxGehy3CfzHydxYObxX+gyHiiyYOkzIWmz4unyoOt1Jeqz5Ku0pOv05e3\n06G415u72KK52KS82p+/3Ka+3KjD267C26nE3KvH3rPG37bJ47fK5LzT5b/X6cnY7MPb7c7a6NDd\n69Xh79/n8OXu9+v0/PD2+PL3+f7//P//////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////\n/////////////////////////////////////////////////////yH+EUNyZWF0ZWQgd2l0aCBH\nSU1QACH5BAEKAP8ALAAAAAAyABQAAAj+AFv9G0iwoMGDCBMqXMiwocOHECNGzNMDCJAeOXL82LgD\nzMBOOEr4McgKzQ8SHz6M8KFoYKsyNkBciKBhxQOBBgWBEfPlx4wbMKJcwfJmIB4OI7YULGXBw4YQ\nP5ooiYHThwIFHpZoaRKjD0MmPnUcXHUITSmCpWR8CLHD08FLCSYYQBVRyo8dPRziWTthE0INExIk\nkihlyA8gBU8ZurOmSp6BkySM2MAooQLAGlRFpGJYSMFAZEqIRjNQzggSIzAltHRZAwhKEKvkGOLZ\nIBcWJc4MNEMiRYmFhQBMuKAgxRRIDa/oyHHk4BzcaXb3/r3w1BgZCi5MGBCJYZYeOprAG7TDgsWa\ngXFIiK7k8FOAmQUKLcxykclBOixaqBn4yEKJEew5BIoCETTQxUJcCAGEEfe1AMN+A8Gh3gg4uTSI\nGZUVlIkGgI2xEBhCCPHEfTDAwAZBpLSAmxcEccLDBBYkQAgoA43CxwQTHODIQmIcIQQSB9lRohsF\niUKAaDcIQUQJAgCiCR4OpLDDDSVMoEECkjCkhhhghHGQH0cc8VhBqZgxBA0l0GBFKAQtAoUMIYzg\nQhLySWTnnXjmqeeeDwUEADs=\n'
TIOBE_ICON_RAW = b'R0lGODlhEgESAef/ACEfIiMfHiIgIyMhJCUhICQiJiUjJiMkLCYkJygkIyQlLSAnLSUmLScmKSYn\nLicnLx8qNCgoMCUpNCMqMSgpMSArNSspLCwqLSIsNycrNy0rLyAuPSQuOS8uMSUwOyIxQCA0RzAx\nOR43UCQ3Sx84UTY0NyU4TCA5UjE4PyI7VCM8VSQ9VSU9Vh8/XDk6QiA/XSY+VyFAXh1EZyNDYT0+\nRiVEYjpBSB9GaSFIaz5FTCRKbSVLbh5NdR9OdkJJUENKUSNQeUNOWR5VgylTgh9WhCpUgyJWikZQ\nXCtVhENSYkhSXkRTYyRZhy5XhidZjkZUZUJVakNWa0pVYSlbj0RXbCpckCtdkSJfmSxekiNgmk5Z\nZSVhmyZinBtlpFFcaB1mplJdaSlknh9np1NeaixloCNpqSRqqhlutFVkdShsrAl0wFdldx1wtlhm\neA51wR9xtyFyuBF2wiNzuRV3wyV0uhd4xF1sfhp5xSp1wh16xh97x2BvgSF8yDB4xjl3uSN9yTJ5\nxyV+yid/zCmAzWd2iDuCyWt6jDyDyj6Eyz+FzTWJ0ECGzjeK0TiL0nOClEWMzXWElk+LyEeNz0iO\n0EqQ0kyR002S1E6T1U+U1neOnn6Nn1mV0lqW01KZ1VyX1FSa1l2Y1Vac2IaVqFme21+d1IGYqWOg\n14uarWWi2Yybrmil3I+fsZGhs3Gn2ZKitHOp25Skt4+muJaluHar3Xes35inunmu4YOt1JuqvYCv\n3IKx3pivwIW04puyw46334+44KW1yJC64aa2yZG74pq615K85JO95ZS+5q690Z3C5LC/057D5Z/E\n56HF6KTI67fH2qzM6q3N67zL37DQ7cPP3bfT6rrW7sjU4r3Z8cvX5cDb887a6MXd8Mff8dHd68nh\n89Dg9NTg79Dk8Nfj8djk89nl9Nrn9d/n8OLn6tzo9uPo693p9+Dp8d/r+ePs9OTt9ejw+enx+urz\n++v0/Oz1/e/19/D2+PL3+fT5/PX6/fb7/vf9//j+//n///7//P///yH+EUNyZWF0ZWQgd2l0aCBH\nSU1QACH5BAEKAP8ALAAAAAASARIBAAj+AP8JHEiwoMGDCBMqXMiwocOHEPUAgkixosWLGDNq3Mix\no8eGEgFN/EiypMmTKFOqjCiy5cqXMGPKnLkyZEuRNHPq3Mlzp82bOHsKHUq0KMWfQIMaXcq0qc+k\n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\nEYiCqEJ6cCUCAQEAOw==\n'


def load_config(config_file):
    '''
    Function to load the saved configuration.
    Creates a new one if none exists.
    '''

    tools = []

    try:
        with open(config_file) as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.FullLoader)

        if not 'TICS_VIEWER_URL' in config.keys():
            inform_and_die('Configuration',
                           'Missing required key in the configuration: TICS_VIEWER_URL')

        if not 'TOOLS' in config.keys():
            inform_and_die('Configuration',
                           'Missing required key in the configuration: TOOLS')

        # Reshape tools format
        for tool in config['TOOLS'].keys():
            tools.append({'name': tool, 'path': config['TOOLS'][tool]})

        return tools, config['TICS_VIEWER_URL']

    except FileNotFoundError:
        return {}, 'http://localhost'


def save_config(tree, tics_url, cfg_file, root):
    '''
    Function to save the configuration.
    '''
    config = {'TICS_VIEWER_URL':'', 'TOOLS':{}}

    config['TICS_VIEWER_URL'] = tics_url.get()

    for child in tree.get_children():
        config['TOOLS'][tree.item(child)["values"][0]] = tree.item(child)["values"][1]

    with open(cfg_file.replace('\\', '/'), 'w') as file:
        yaml.dump(config, file)

    root.destroy()
    main()


def inform_and_die(err_kind, message):
    '''
    Function to raise error dialog and die afterwards
    '''
    messagebox.showerror(f'{err_kind} error', message)
    sys.exit(-1)


def edit_config(root, tools, tics_url):
    '''
    Enables the user to edit the configuration.
    Creates a panel for easy editing
    '''

    cfg_window = Toplevel(root)
    cfg_window.title("TiCS Quality Dock Configuration")
    cfg_window.minsize(900, 450)
    cfg_window.iconphoto(False, PhotoImage(data=TIOBE_ICON_RAW))

    tics_label = Label(cfg_window, text="TiCS Viewer URL:")
    tics_label.grid(column=0,
                    row=0,
                    padx=20,
                    pady=20)

    url = Entry(cfg_window, width=100)
    url.insert(END, tics_url)
    url.grid(column=1, row=0, columnspan=2)

    cfg_label = Label(cfg_window, text="Configured tools:")
    cfg_label.grid(column=0,
                   row=1,
                   padx=20,
                   pady=5)

    # Form for inserting new items
    ins_btn = Button(cfg_window,
                     text='Update',
                     width=10,
                     command=lambda: insert(tree, new_name, new_path, cfg_window))
    ins_btn.grid(column=0, row=2)

    new_name = Entry(cfg_window, width=25)
    new_name.grid(column=1, row=2)

    new_path = Entry(cfg_window, width=75)
    new_path.grid(column=2, row=2)

    rem_btn = Button(cfg_window,
                     text='Remove',
                     width=10,
                     command=lambda: remove(tree))
    rem_btn.grid(column=0, row=3)

    tree = ttk.Treeview(cfg_window)
    tree['show'] = 'headings'
    tree.grid(column=1, row=3, columnspan=2, sticky='nsew')

    tree['columns'] = ('name', 'path')
    tree.column('name', width=150, anchor='center')
    tree.heading('name', text='Name')

    tree.column('path', width=450, anchor='center')
    tree.heading('path', text='Path')

    for tool in tools:
        tree.insert('', 'end', text=tool['name'], values=[tool["name"], tool["path"]])

    open_btn = Button(cfg_window,
                      text='Browse',
                      width=10,
                      command=lambda: open_file(new_name, new_path, cfg_window))
    open_btn.grid(column=4, row=2, padx=20)

    save_btn = Button(cfg_window,
                      text='Save',
                      width=10,
                      command=lambda: save_config(tree, url, CFG_FILE, root))
    save_btn.grid(column=0, row=4)

    close_btn = Button(cfg_window,
                       text='Close',
                       width=10,
                       command=lambda: close_window(cfg_window))
    close_btn.grid(column=0, row=5, pady=5)

    tree.bind("<<TreeviewSelect>>", lambda event,
                                           tree=tree,
                                           new_name=new_name,
                                           new_path=new_path: tree_select(tree, new_name, new_path))


def tree_select(tree, new_name, new_path):
    '''
    Makes sure selected tree item is reflected in the
    enyry boxes.
    '''

    if tree.selection():
        new_name.delete(0, END)
        new_path.delete(0, END)
        name, path = tree.item(tree.selection(), "values")

        new_name.insert(END, name)
        new_path.insert(END, path)


def open_file(name_obj, path_obj, master):
    '''
    For easy selection of files from the file system
    '''

    file = filedialog.askopenfilename(parent=master, initialdir="/", title="Select file")
    path_obj.delete(0, END)
    name_obj.delete(0, END)
    path_obj.insert(END, file)
    name_obj.insert(END, ntpath.basename(file).replace('.exe', '').capitalize())


def close_window(windows):
    '''
    Helper function for destruction of windows
    '''
    windows.destroy()


def insert(tree, new_name, new_path, cfg_window):
    '''
    Insertion of items in the treeview
    '''

    new_name_str = new_name.get()
    new_path_str = new_path.get().replace('\\', '/')
    selected_item = tree.selection()
    item_exists = False
    position = END

    if not new_name_str:
        messagebox.showerror(f'Validation', 'Name cannot be empty', parent=cfg_window)
    elif not new_path_str:
        messagebox.showerror(f'Validation', 'Path cannot be empty', parent=cfg_window)
    else:
        # Check if entry already exists
        for child in tree.get_children():

            if(tree.item(child)["values"][0] == new_name_str and
               tree.item(child)["values"][1] == new_path_str):
                item_exists = True

        # Input is the same as tree content
        if(item_exists and not selected_item):
            #duplicate
            messagebox.showerror(f'Validation', 'Cannot add duplicate entry', parent=cfg_window)
            return

        else:
            #update item
            position = tree.index(tree.focus())
            remove(tree)

        tree.insert('', position, text=new_name_str, values=[new_name_str, new_path_str])


def remove(tree):
    '''
    Removal of treeview items
    '''

    selected_item = tree.selection() ## get selected item
    if selected_item:
        tree.delete(selected_item[0])


def run_tics_viewer(url):
    '''
    Open the TICS viewer URL
    '''

    message = f'The following configured URL is not valid:\n"{url}"\n\nPlease check your configuration'

    if is_url(url):
        open_url(url)
    else:
        messagebox.showerror(f'Validation', message)


def open_url(url):
    if sys.platform == "win32":
            os.startfile(url)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, url])

def run_tool(tool):
    '''
    Run configured executable or open URL in browser.
    Takes platform in account
    '''
    message = f'The following configured path does not exist:\n"{tool}"\n\nPlease check your configuration'

    if os.path.isfile(tool):
        if sys.platform == "win32":
            os.startfile(tool)
        elif os.access(tool, os.X_OK):
            subprocess.Popen(tool)
        else:
            subprocess.call(["xdg-open", tool])
    elif is_url(tool):
        open_url(tool)
    else:
        messagebox.showerror(f'Validation', message)

def is_url(url):
    '''
    Check URL is valid
    '''
    regex = '^(http|https):\/\/[a-zA-Z0-9]*(:\d{2,5})\/([a-zA-Z0-9])?|^(http|https):\/\/[a-zA-Z0-9]*$|^(http|https):\/\/([a-zA-Z0-9]*\.){1,3}.\w+'
    
    match = re.match(regex, url)
    
    if not match or len(url.replace('http://','').replace('https://','').split(':')) > 2:
        return None
    
    return match


def main():
    '''
    Main function responsible for creating the main panel
    '''

    # Fix distro mismatch on linux
    if 'LD_LIBRARY_PATH' in os.environ.keys():
        os.environ.pop('LD_LIBRARY_PATH')

    tools, tics_url = load_config(CFG_FILE.replace('\\', '/'))
    longest = 0

    for tool in tools:
        longest = len(tool['name']) if len(tool['name']) > longest else longest

    dock_width = max(170 + 7 * longest, 300)
    dock_height = 100 + 20*len(tools)

    ext_tool_row = 1

    # create root window
    root = Tk()
    root.tk.call('tk', 'scaling', 1.5)
    tics_logo = PhotoImage(data=TICS_LOGO_RAW)

    # root window title and dimension
    root.title("TiCS Quality Dock")
    root.geometry(f'{dock_width}x{dock_height}')
    root.iconphoto(False, PhotoImage(data=TIOBE_ICON_RAW))

    # adding menu bar in root window
    menubar = Menu(root)
    options_menu = Menu(menubar, tearoff=0)
    options_menu.add_command(label="Configure", command=lambda: edit_config(root, tools, tics_url))
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=options_menu)

    tics_label = Label(root, text="TiCS Viewer")
    tool_label = Label(root, text="Tools")

    tics_label.grid(column=0,
                    row=0,
                    padx=20,
                    pady=5)

    tool_label.grid(column=1,
                    row=0,
                    padx=20,
                    pady=5)

    tics_btn = Button(root,
                      text="TICS Viewer",
                      image=tics_logo,
                      command=lambda: run_tics_viewer(tics_url))

    tics_btn.grid(column=0,
                  row=1,
                  padx=20,
                  pady=2)

    for idx in range(0, len(tools)):
        btn = Button(root,
                     text=tools[idx]['name'],
                     width=longest,
                     height=1,
                     command=lambda idx=idx: run_tool(tools[idx]['path']))

        btn.grid(column=1,
                 row=ext_tool_row,
                 padx=20,
                 pady=2)

        ext_tool_row += 1

    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
