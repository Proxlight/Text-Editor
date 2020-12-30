from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.messagebox import *


class Edit():
    def popup(self, event):
        self.rightClick.post(event.x_root, event.y_root)

    def copy(self, *args):
        sel = self.text.selection_get()
        self.clipboard = sel

    def cut(self, *args):
        sel = self.text.selection_get()
        self.clipboard = sel
        self.text.delete(SEL_FIRST, SEL_LAST)

    def paste(self, *args):
        self.text.insert(INSERT, self.clipboard)

    def selectAll(self, *args):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(0.0, END)
        self.text.see(INSERT)

    def undo(self, *args):
        self.text.edit_undo()

    def redo(self, *args):
        self.text.edit_redo()

    def find(self, *args):
        self.text.tag_remove('found', '1.0', END)
        target = askstring('Find', 'Search String:')

        if target:
            idx = '1.0'
            while 1:
                idx = self.text.search(target, idx, nocase=1, stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(target))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', foreground='white', background='blue')

    def __init__(self, text, root):
        self.clipboard = None
        self.text = text
        self.rightClick = Menu(root)


def main(root, text, menubar):

    objEdit = Edit(text, root)

    editmenu = Menu(menubar)
    editmenu.add_command(label="Copy", command=objEdit.copy, accelerator="Ctrl+C")
    editmenu.add_command(label="Cut", command=objEdit.cut, accelerator="Ctrl+X")
    editmenu.add_command(label="Paste", command=objEdit.paste, accelerator="Ctrl+V")
    editmenu.add_command(label="Undo", command=objEdit.undo, accelerator="Ctrl+Z")
    editmenu.add_command(label="Redo", command=objEdit.redo, accelerator="Ctrl+Y")
    editmenu.add_command(label="Find", command=objEdit.find, accelerator="Ctrl+F")
    editmenu.add_separator()
    editmenu.add_command(label="Select All", command=objEdit.selectAll, accelerator="Ctrl+A")
    menubar.add_cascade(label="Edit", menu=editmenu)

    root.bind_all("<Control-z>", objEdit.undo)
    root.bind_all("<Control-y>", objEdit.redo)
    root.bind_all("<Control-f>", objEdit.find)
    root.bind_all("Control-a", objEdit.selectAll)

    objEdit.rightClick.add_command(label="Copy", command=objEdit.copy)
    objEdit.rightClick.add_command(label="Cut", command=objEdit.cut)
    objEdit.rightClick.add_command(label="Paste", command=objEdit.paste)
    objEdit.rightClick.add_separator()
    objEdit.rightClick.add_command(label="Select All", command=objEdit.selectAll)
    objEdit.rightClick.bind("<Control-q>", objEdit.selectAll)

    text.bind("<Button-3>", objEdit.popup)

    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")
