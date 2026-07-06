from tkinter import Entry, N


class TkinterEntry(Entry):
    '''
    The entry class includes the constructor method to automatically assign a borderless entry
    for typing and press buttons to write expressions. By default: an instance of the TkinterEntry class
    will place the entry field toward the top of the calculator. By using a normal configuration,
    I'm allowing who ever is using the calculator to interact with the field.
    '''
    def __init__(self, tk, bg='#f2f2f2', fg='#000000', font=('roboto', 24), relief='ridge', bd=0, highlightthickness=0, **kwargs):
        Entry.__init__(self, tk, bg='#f2f2f2', fg='#000000', font=('roboto', 24), relief='flat', bd=0, highlightthickness=0, **kwargs)
        self.place(relx=0.5, rely=0.1, height=70, width=390, anchor=N)
        self.config(state='normal')
        
        
        