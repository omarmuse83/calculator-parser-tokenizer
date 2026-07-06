from tkinter import N, Button
from tkinterbuttonplacement import TkinterButtonPlacement
from tkinterentry import TkinterEntry
from tkinterinstance import TkinterInstance


def tkinter_main():
    ''' Purpose of the function is to integrate Tkinter classes into a main function.
        Inside the calculator is a borderless entry field in which you can type
        mathematical expressions/terms.
    '''
    tk = TkinterInstance()
    tkinter_entry = TkinterEntry(tk)
    button_placement = TkinterButtonPlacement(tk, tkinter_entry)
    tkinter_entry.bind('<Return>', lambda event: button_placement.tkinter_event('=', tkinter_entry, tk))
    tkinter_entry.bind('<Key>', lambda event: button_placement.color_change(tkinter_entry))
    tk.mainloop()
    
    
    
    
tkinter_main()


