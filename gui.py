from tkinter import *
from nli import *



def gui():
    window = Tk()
    window.geometry('700x200')
    window.title("NLI GUI")

    lbl1 = Label(window, text="Please enter NLI query", font=("Arial Bold", 30))
    lbl1.grid(column=0, row=0)

    txt = Entry(window, width=50)
    txt.grid(column=0, row=1)
    txt.focus()

    def clicked():
        res = txt.get()
        sql_command = nli_func(res)
        output = sql_command # delete
        #TODO:call on db using sql
        #output = sql(sql_command)
        lbl2.configure(text=output)

    btn = Button(window, text="Click Me", highlightbackground='#3E4149', command=clicked)
    btn.grid(column=0, row=2)
    lbl2 = Label(window, text="", font=("Arial Bold", 12))
    lbl2.grid(column=0, row=3)

    window.mainloop()

if __name__ == '__main__':
    gui()