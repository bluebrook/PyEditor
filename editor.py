from Tkinter import *
import tkFileDialog,tkMessageBox
import os
import traceback
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

def hello():
    pass

class Editor(object):
    STYLE = "default"
    TITLE = "nodepad_py"
    def __init__(self, master):
        self.root = master
        self.file_path = None
        self.editor = None
        self.text = None

        self.frame = Frame(self.root)
        self.add_widgets()

    def set_title(self, event=None):
        """ set Editor file path"""
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def add_widgets(self):
        self.set_title()
        self.yscrollbar = Scrollbar(self.frame, orient="vertical")
        self.editor = Text(self.frame, yscrollcommand=self.yscrollbar.set)
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.config(wrap="word",  # use word wrapping
                           undo=True,  # Tk 8.4
                           width=80)
        self.editor.focus()
        self.yscrollbar.pack(side="right", fill="y")
        self.yscrollbar.config(command=self.editor.yview)
        self.frame.pack(fill="both", expand=1)

        self.syntax_highlight_init()
        self.add_menu()


    def add_menu(self):
        # instead of closing the window, execute a function
        self.root.protocol("WM_DELETE_WINDOW", self.file_quit)

        # create a top level menu
        self.menubar = Menu(root)
        # Menu item File
        filemenu = Menu(self.menubar, tearoff=0)  # tearoff = 0 => can't be seperated from window
        filemenu.add_command(label="New", underline=1, command=self.file_new, accelerator="Ctrl+N")
        filemenu.add_command(label="Open...", underline=1, command=self.file_open, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", underline=1, command=self.file_save, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...", underline=5, command=self.file_save_as, accelerator="Ctrl+Alt+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=2, command=self.file_quit, accelerator="Alt+F4")
        self.menubar.add_cascade(label="File", underline=0, menu=filemenu)

        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Cut", underline=1, command=hello)
        editmenu.add_command(label="Copy", underline=1, command=self.edit_copy, accelerator="Ctrl+C")
        editmenu.add_command(label="Paste", underline=1, command=self.edit_paste, accelerator="Ctrl+V")
        self.menubar.add_cascade(label="Edit", underline=1, menu=editmenu)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About", command=hello)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        # display the menu
        self.root.config(menu=self.menubar)

        self.editor.bind("<Control-o>", self.file_open)
        self.editor.bind("<Control-O>", self.file_open)
        self.editor.bind("<Control-S>", self.file_save)
        self.editor.bind("<Control-s>", self.file_save)
        self.editor.bind("<Control-y>", self.redo)
        self.editor.bind("<Control-Y>", self.redo)
        self.editor.bind("<Control-Z>", self.undo)
        self.editor.bind("<Control-z>", self.undo)
        self.editor.bind("<KeyRelease>", self.syntax_highlight_update)

    def syntax_highlight_init(self):
        style = get_style_by_name(self.STYLE)
        for t, s in style:
            name = str(t)
            for k,v in s.iteritems():
                if k == "color" and v:
                    self.editor.tag_configure(name, foreground="#{}".format(v))
                elif k == "bgcolor" and v:
                    pass #self.editor.tag_configure(name, background="#{}".format(v))

        """self.editor.tag_configure("Token.Keyword", foreground="orange")
        self.editor.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        self.editor.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        self.editor.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
        self.editor.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        self.editor.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
        self.editor.tag_configure("Token.Keyword.Type", foreground="#CC7A00")
        self.editor.tag_configure("Token.Name.Class", foreground="red")
        self.editor.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.editor.tag_configure("Token.Name.Function", foreground="blue")
        self.editor.tag_configure("Token.Operator.Word", foreground="#CC7A00")
        self.editor.tag_configure("Token.Comment", foreground="gray")
        self.editor.tag_configure("Token.Literal.String", foreground="green")"""


    def syntax_highlight_update(self,event=None):
        self.editor.mark_set("range_start", "1.0")
        data = self.editor.get("1.0", "end-1c")
        print data
        for token, content in lex(data, PythonLexer()):
            print str(token)
            self.editor.mark_set("range_end", "range_start + %dc" % len(content))
            self.editor.tag_add(str(token), "range_start", "range_end")
            self.editor.mark_set("range_start", "range_end")

    def add_text(self):
        self.text = Text(self.root, wrap="none", width=50, height = 100)
        xscrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        yscrollbar = Scrollbar(self.root)
        yscrollbar.pack(side=RIGHT, fill=Y)

        self.text.config(
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set)
        xscrollbar.config(command=self.text.yview)
        yscrollbar.config(command=self.text.xview)

        self.text.pack()

    def xfile_open(self):
        myfiletypes = [('Python files', '*.py'), ('All files', '*')]
        filename = tkFileDialog.askopenfilename(title="open a file")
        #filename = tkFileDialog.Open(self.root, filetypes=myfiletypes)
        print filename

        with open(filename, "r") as OF:
            #print OF.read()
            self.text.insert("1.0", OF.read())

    def xfile_save(self):
        out_file = tkFileDialog.asksaveasfile(title="save as")
        out_file.write(self.text.get("1.0", END))

    def Edit(self):
        pass

    def say_hi(self):
        print "hi there, everyone!"

    def save_if_modified(self, event=None):
        if self.editor.edit_modified():  # modified
            response = tkMessageBox.askyesnocancel("Save?",
                                                 "This document has been modified. Do you want to save changes?")  # yes = True, no = False, cancel = None
            if response:  # yes/save
                result = self.file_save()
                if result == "saved":  # saved
                    return True
                else:  # save cancelled
                    return None
            else:
                return response  # None = cancel/abort, False = no/discard
        else:  # not modified
            return True

    def file_new(self, event=None):
        result = self.save_if_modified()
        if result != None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            self.editor.delete(1.0, "end")
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.file_path = None
            self.set_title()

    def file_open(self, event=None, filepath=None):
        result = self.save_if_modified()
        if result != None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            if filepath == None:
                filepath = tkFileDialog.askopenfilename()
            if filepath != None and filepath != '':
                with open(filepath,"r") as f:
                    fileContents = f.read()  # Get all the text from file.
                # Set current text to file contents
                self.editor.delete(1.0, "end")
                self.editor.insert(1.0, fileContents)
                self.editor.edit_modified(False)
                self.file_path = filepath
        self.syntax_highlight_update()

    def file_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(filepath=self.file_path)
        return result

    def file_save_as(self, event=None, filepath=None):
        if filepath == None:
            filepath = tkFileDialog.asksaveasfilename(filetypes=(
            ('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*')))  # defaultextension='.txt'
        try:
            with open(filepath, 'wb') as f:
                text = self.editor.get(1.0, "end-1c")
                f.write(bytes(text))
                self.editor.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return "saved"
        except Exception as e:
            traceback.print_exc()
            print e
            print 'FileNotFoundError'
            return "cancelled"

    def file_quit(self, event=None):
        result = self.save_if_modified()
        if result != None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            self.root.destroy()  # sys.exit(0)

    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def undo(self, event=None):
        self.editor.edit_undo()

    def redo(self, event=None):
        self.editor.edit_redo()

    def edit_copy(self):
        text = self.editor.get(SEL_FIRST, SEL_LAST)
        self.root.clipboard_clear()
        # text to clipboard
        self.root.clipboard_append(text)

    def edit_paste(self):
        self.editor.insert(INSERT, root.clipboard_get())

root = Tk()
e = Editor(root)
e.frame.mainloop()