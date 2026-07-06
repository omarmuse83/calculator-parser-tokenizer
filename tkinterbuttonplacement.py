from tkinter import StringVar, Button, END
import string
from evaluate import EvaluateExpression
class TkinterButtonPlacement:
    def __init__(self, tk, entry):
        '''
        The constructor method initalizes a dictionary variable, expression string, and a button list.
        The tkinter_event method handles what happens when certain events are triggered within the calculator.
        For example: when the user presses the equal button on the calculator, the custom parser & tokenizer breaks the expression
        into a series of tokens, and determines the first operator, first number, and second number, and evaluates that
        sub portion of the expression before moving onto other expressions.
        
        The color change method of the class handles what happens when the user encounters an 'invalid operation' or an
        expression that is too large. In this case: the calculator is highlighted in a shade of red, and when the user types anything else,
        the color changes back to its default black.
        '''
        self.d1 = {f'{i}': StringVar(tk, i) for i in range(0, 10)}
        self.d2 = {'CE': StringVar(tk, 'CE'), '*': StringVar(tk, '*'), '/': StringVar(tk, '/'), '+': StringVar(tk, '+'), '-': StringVar(tk, '-'), '^': StringVar(tk, '^'), '.': StringVar(tk, '.'), '(': StringVar(tk, '('), ')': StringVar(tk, ')'), '=': StringVar(tk, '='), '⌫': StringVar(tk, '⌫')}
        self.dictionary_variable = self.d1 | self.d2
        self.expression_string = ''
        self.button_list = [Button(tk, text="1", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['1'], command=lambda: self.tkinter_event('1', entry, tk)).place(height=45, width=70, relx=0.05, rely=0.70),
                        Button(tk, text="2", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['2'], command=lambda: self.tkinter_event('2', entry, tk)).place(height=45, width=70, relx=0.30, rely=0.70),
                        Button(tk, text="3", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['3'], command=lambda: self.tkinter_event('3', entry, tk)).place(height=45, width=70, relx=0.55, rely=0.70),
                        Button(tk, text="4", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['4'], command=lambda: self.tkinter_event('4', entry, tk)).place(height=45, width=70, relx=0.05, rely=0.57),
                        Button(tk, text="5", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['5'], command=lambda: self.tkinter_event('5', entry, tk)).place(height=45, width=70, relx=0.30, rely=0.57),
                        Button(tk, text="6", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['6'], command=lambda: self.tkinter_event('6', entry, tk)).place(height=45, width=70, relx=0.55, rely=0.57),
                        Button(tk, text="7", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['7'], command=lambda: self.tkinter_event('7', entry, tk)).place(height=45, width=70, relx=0.05, rely=0.44),
                        Button(tk, text="8", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['8'], command=lambda: self.tkinter_event('8', entry, tk)).place(height=45, width=70, relx=0.30, rely=0.44),
                        Button(tk, text="9", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['9'], command=lambda: self.tkinter_event('9', entry, tk)).place(height=45, width=70, relx=0.55, rely=0.44),
                        Button(tk, text="CE", font='roboto', cursor='hand1', activebackground='#fccdc9', bg='#F88379', relief='flat', textvariable=self.dictionary_variable['CE'], command=lambda: self.tkinter_event('CE', entry, tk)).place(height=55, width=70, relx=0.78, rely=0.30),
                        Button(tk, text="(", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['('], command=lambda: self.tkinter_event('(', entry, tk)).place(height=45, width=70, relx=0.30, rely=0.30),  
                        Button(tk, text=")", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable[')'], command=lambda: self.tkinter_event(')', entry, tk)).place(height=45, width=70, relx=0.55, rely=0.30),
                        Button(tk, text="X", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['*'], command=lambda: self.tkinter_event('*', entry, tk)).place(height=45, width=70, relx=0.78, rely=0.55),
                        Button(tk, text="/", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['/'], command=lambda: self.tkinter_event('/', entry, tk)).place(height=45, width=70, relx=0.78, rely=0.65),
                        Button(tk, text="+", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['+'], command=lambda: self.tkinter_event('+', entry, tk)).place(height=45, width=70, relx=0.78, rely=0.75),
                        Button(tk, text="-", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['-'], command=lambda: self.tkinter_event('-', entry, tk)).place(height=45, width=70, relx=0.78, rely=0.85),
                        Button(tk, text="^", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['^'], command=lambda: self.tkinter_event('^', entry, tk)).place(height=45, width=70, relx=0.78, rely=0.45),
                        Button(tk, text="=", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['='], command=lambda: self.tkinter_event('=', entry, tk)).place(height=45, width=70, relx=0.55, rely=0.83),
                        Button(tk, text="0", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['0'], command=lambda: self.tkinter_event('0', entry, tk)).place(height=45, width=70, relx=0.05, rely=0.83),
                        Button(tk, text=".", font='roboto', cursor='hand1', activebackground='#e1dfdd', bg='#faf8f6', relief='flat', textvariable=self.dictionary_variable['.'], command=lambda: self.tkinter_event('.', entry, tk)).place(height=45, width=60, relx=0.31, rely=0.83),
                        Button(tk, text="⌫", font='roboto', cursor='hand1', activebackground='#fccdc9', bg='#F88379', relief='flat', textvariable=self.dictionary_variable['⌫'], command=lambda: self.tkinter_event('⌫', entry, tk)).place(height=55, width=70, relx=0.05, rely=0.30)
                    ]
    def tkinter_event(self, new_event, entry, tk):
        entry.config(fg='#000000')
        new_call = self.dictionary_variable[new_event].get()
        if new_call not in ['⌫', 'CE', '=']:
            self.expression_string += new_call
        if (new_call == '⌫'):
            if (entry.get() == 'invalid operation') or ('expression' in entry.get()):
                self.expression_string = 'invalid operation'
            self.expression_string = self.expression_string[:len(self.expression_string)-1]
            if len(entry.get()) >= 1:
                entry.config(state='normal')
                if entry.get()[-1] != ' ':
                    entry.delete((len(entry.get())-1), END)
                elif entry.get()[-1] == ' ':
                    if entry.get()[-1] == ' ' and entry.get()[-3] == ' ':
                        entry.delete((len(entry.get())-3), END)
                    else:
                        entry.delete((len(entry.get())-2), END)
        elif new_call == 'CE':
            self.expression_string = ''
            entry.delete(0, END)
        elif ((len(entry.get()) >= 1) and (new_call == '=')):
            self.expression_string = entry.get()
            entry.delete(0, END)
            entry.insert(END, EvaluateExpression().evaluate(self.expression_string))
            if (EvaluateExpression().evaluate(self.expression_string) == 'invalid operation') or ('expression/result too large' in str(EvaluateExpression().evaluate(self.expression_string))):
                entry.config(fg='#880808')
            else:
                self.expression_string = str(EvaluateExpression().evaluate(self.expression_string))
            
            # Incomplete, must work on the equaling logic of this project.
        elif ((new_call != 'CE')):
            if new_event not in string.digits+'.'+'('+')':
                if new_event != '=':
                    entry.insert(END, ' '+new_event+' ')
            elif new_event in string.digits+'.'+'('+')':
                entry.insert(END, new_event)
        if (EvaluateExpression().evaluate(self.expression_string) != 'invalid operation') and ('expression/result' not in str(EvaluateExpression().evaluate(self.expression_string))):
            print(EvaluateExpression().evaluate(self.expression_string))
    def color_change(self, entry):
        entry.config(fg='#000000')
        

            
            
            
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                
