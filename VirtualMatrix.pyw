#python

import tkinter
import numpy as np


class Dot:
    def __init__(self, canvas, x0, y0, x1, y1):
        #Create the circle
        self.canvas = canvas
        self.dotID = canvas.create_oval(x0,y0,x1,y1, fill='#bfbfbf', outline='', tags="unclicked")
        #Define the action that will be executed at click on a dot
        canvas.tag_bind(self.dotID, "<Button-1>", self.GetPressed)

    def GetPressed(self, event):
        if (self.canvas.gettags(self.dotID)[0]=="unclicked"):
            self.canvas.itemconfig(self.dotID, fill='red', tags="clicked")
        elif (self.canvas.gettags(self.dotID)[0]=="clicked"):
            self.canvas.itemconfig(self.dotID, fill='#bfbfbf', tags="unclicked")

    def ReturnID(self):
        return self.dotID


class LEDMatrix:
    dot_dia = 15
    window_border = 20
    dot_whitespace = 5
 
    def __init__(self, window, dots, matrices):
        self.rows = dots
        self.colums = dots
        self.matrices = matrices
        self.dot_array = np.zeros((self.rows,self.matrices,self.colums), dtype=int)
        window_width = 2*self.window_border+self.rows*matrices*self.dot_dia+(self.rows*matrices-1)*self.dot_whitespace
        window_height = 2*self.window_border + self.colums*self.dot_dia + (self.colums-1)*self.dot_whitespace
        self.canvas = tkinter.Canvas(window, width=window_width, height=window_height)
        self.canvas.pack()

    def plot_matrix(self):
        for k in range(0,self.rows,1):
            for j in range(0,self.matrices,1):
                for i in range(0,self.colums,1):
                    #Define the edge values of the circle
                    x0 = self.window_border + (self.colums*j+i)*(self.dot_dia + self.dot_whitespace)
                    y0 = self.window_border + k*(self.dot_dia + self.dot_whitespace)
                    x1 = x0 + self.dot_dia
                    y1 = y0 + self.dot_dia
                    #Create the circle object
                    self.newdot = Dot(self.canvas,x0,y0,x1,y1)
                    self.dot_array[k,j,i]=Dot.ReturnID(self.newdot)

    def ReturnClickedDots(self):
        self.OutputArray = np.zeros((self.matrices,self.rows), dtype=int)
        self.SelectedList = self.canvas.find_withtag("clicked")
        for rows in range(0,self.rows,1):
                for matrices in range(0,self.matrices,1):
                    for colums in range(0,self.colums,1):
                        if (self.dot_array[rows,matrices,colums] in self.SelectedList):
                            self.OutputArray[matrices,rows] = int(self.OutputArray[matrices,rows]) | int(1<<colums)
        #Create the output window
        sub_window = tkinter.Tk()
        textfield = tkinter.Text(sub_window, height=20, width=80)
        textfield.pack()
        #Print the c-File
        start_line = "uint8_t insert_name [" + str(int(len(self.OutputArray))) + "][" + str(int(len(self.OutputArray[0]))) + "] = {\n"
        textfield.insert(tkinter.END, start_line)
        for matrices in range(0,self.matrices,1):
            textfield.insert(tkinter.END, "\t{")
            for colums in range(0,self.colums,1):
                if ((colums != self.colums-1)):
                    print_line = str(hex(self.OutputArray[matrices][colums])) +",\t"
                elif (colums == self.colums-1):
                    print_line = str(hex(self.OutputArray[matrices][colums])) +"}"
                textfield.insert(tkinter.END, print_line)
            textfield.insert(tkinter.END, ",\n")
        textfield.insert(tkinter.END, "};")

main_window = tkinter.Tk()
           
matrix = LEDMatrix(main_window, 8,1)
matrix.plot_matrix()
button = tkinter.Button(text="Gibs aus", command=matrix.ReturnClickedDots)
button.pack()

main_window.mainloop()
