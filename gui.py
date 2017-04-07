'''

A. Interpolation

    Chebyshev
    Splines (cubic)
    Bezier
    
B. Least Squares

    Linear
    Nonlinear
    
C. Differentiation and Integration

    Differentiation
    Difference Methods
    Extrapolation
    Automatic Differentiation (professor's notes/references)
    Integration
    Newton-Codes - Trapezoidal, Simpson
    Romberg
    Adaptive
    Gaussian
    
'''

import time
from Tkinter import *
from ttk import *
from chebyshev import Chebyshev
import math
from universal_function import f
import numpy
import importlib

class App(Frame):
    def __init__(self):
        self.root = Tk()
        self.root.s = Style()
        self.root.geometry("420x300")
        self.root.resizable(0,0)
        self.root.s.theme_use("clam")
        self.root.title("Numerical Analysis - Project 2")
        
        Frame.__init__(self, self.root)
        self.createWidgets()
        
    def wait(self):
        while not w.can_make_request():
            time.sleep(1)

    def createWidgets(self):
        
        # Interpolation Frame        
        self.interpLabelframe = LabelFrame(self.root, text = "Interpolation", labelanchor = N)
        self.interpLabelframe.grid(row = 0, columnspan = 7, sticky = 'WE', \
                                   padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.interpLabelframe.pack(fill = 'both', expand = 'yes')
        self.innerInFrame = Frame(self.interpLabelframe)
        self.innerInFrame.grid(padx=1)
        
        # Interpolation Frame Buttons
        self.chebyButton = Button(self.innerInFrame, text = "Chebyshev", width=20, command = self.chebyWindow)
        self.splinesButton = Button(self.innerInFrame, text = "Splines (cubic)", width=20, command = self.splinesWindow)
        self.bezierButton = Button(self.innerInFrame, text = "Bezier", width=21, command = self.bezierWindow)
        self.chebyButton.grid(row = 0, column = 0)
        self.splinesButton.grid(row = 0, column = 1)
        self.bezierButton.grid(row = 0, column = 2)

        # Least Squares Frame
        self.lsLabelframe = LabelFrame(self.root, text = "Least Squares", labelanchor = N)
        self.lsLabelframe.grid(row = 2, sticky = 'WE', \
                               padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.lsLabelframe.pack(fill = 'both', expand = 'yes')
        self.innerLsFrame = Frame(self.lsLabelframe)
        self.innerLsFrame.grid(padx = 118)
        
        # Least Squares Frame Buttons
        self.linearBtn = Button(self.lsLabelframe, text = "Linear", width=27)
        self.nonLinBtn = Button(self.lsLabelframe, text = "Nonlinear", width=27)
        self.linearBtn.grid(row = 0, column = 0, sticky = W)
        self.nonLinBtn.grid(row = 0, column = 1)

        # Differentiation and Integration Frame
        self.diffAndInt = Frame(self.root)#, text = "Differentiation and Integration", labelanchor = N)
        self.diffAndInt.grid(row = 0, columnspan = 7, sticky = 'WE', \
                                   padx = 5, pady = 5, ipadx = 10, ipady = 5)
        self.diffAndInt.pack(fill = 'both', expand = 'yes')
        
        # Sub Frames
        self.diffFrame = LabelFrame(self.diffAndInt, text = "Differentiation", labelanchor = N)
        self.intFrame = LabelFrame(self.diffAndInt, text = "Integration", labelanchor = N)
        self.diffFrame.grid(row = 0, column = 0, columnspan = 2)
        self.intFrame.grid(row = 1, column = 0)
        self.diffFrame.pack(expand = 'yes')
        self.intFrame.pack(expand = 'yes')
        
        # Differentiation and Integration Buttons
        self.differenceBtn = Button(self.diffFrame, text = "Difference Methods")
        self.extrapBtn = Button(self.diffFrame, text = "Extrapolation", width=20)
        self.autoDiffBtn = Button(self.diffFrame, text = "Automatic Differentiation")
        
        self.newtonCodesBtn = Button(self.intFrame, text = "Newton-Codes", width=20)
        self.rombergBtn = Button(self.intFrame, text = "Romberg", width=20)
        self.adaptBtn = Button(self.intFrame, text = "Adaptive", width=20)

        self.differenceBtn.grid(row = 0, column = 0)
        self.extrapBtn.grid(row = 0, column = 1)
        self.autoDiffBtn.grid(row = 0, column = 2)

        self.newtonCodesBtn.grid(row = 0, column = 0)
        self.rombergBtn.grid(row = 0, column = 1)
        self.adaptBtn.grid(row = 0, column = 2)
        
        # Bottom Frame
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(fill = 'x', side = BOTTOM )

        # Quit
        self.quit = Button(self.bottomFrame, text = "Quit", command = self.quitApp)
        self.quit.pack(fill = 'x')

    def chebyWindow(self):
        # create Chebyshev window
        self.cheby = Toplevel()
        self.cheby.title("Chebyshev")
        self.cheby.resizable(0,0)
        self.chebResult = DoubleVar()
        self.chebErr = DoubleVar()
        mainFrame = Frame(self.cheby)
        mainFrame.pack()

        # Interval Label
        Label(mainFrame, text = "Enter Interval [a, b]:").grid(row = 0, sticky = W)

        # a label and entry box
        aLabel = Label(mainFrame, text = "a:").grid(row = 1, sticky = W)
        aCheb = Entry(mainFrame, width = 40)
        aCheb.grid(row = 1, sticky = W, padx = 50)

        # b label and entry box
        bLabel = Label(mainFrame, text = "b:").grid(row = 2, sticky = W)
        bCheb = Entry(mainFrame, width = 40)
        bCheb.grid(row = 2, sticky = W, padx = 50)

        # degree label and entry box
        dLabel = Label(mainFrame, text = "Degree:").grid(row = 3, sticky = W)
        dCheb = Entry(mainFrame, width = 40)
        dCheb.grid(row = 3, sticky = W, padx = 50)

        # f(x) label and entry box
        fLabel = Label(mainFrame, text = "f(x):").grid(row = 4, sticky = W)
        fCheb = Entry(mainFrame, width = 40)
        fCheb.grid(row = 4, sticky = W, padx = 50)

        # x label and entry box
        xLabel = Label(mainFrame, text="x = ").grid(row=5, sticky=W)
        xCheb = Entry(mainFrame, width=40)
        xCheb.grid(row=5, sticky=W, padx=50)

        # Submit Button
        submitBtn = Button(mainFrame, text = "Submit", command = lambda: self.doCheby(aCheb.get(), bCheb.get(), dCheb.get(), fCheb.get(), xCheb.get()))
        submitBtn.grid(row = 6, pady = 10)

        # Result Label and Result Box 
        Label(mainFrame, text = "Result:").grid(row = 7, sticky = W)
        resultMsg = Entry(mainFrame, width = 40, textvariable = self.chebResult)
        resultMsg.grid(row = 7, sticky = W, padx = 50)

        # Error Label and Result Box
        Label(mainFrame, text = "Error:").grid(row = 8, sticky = W)
        errMsg = Entry(mainFrame, width = 40, textvariable = self.chebErr)
        errMsg.grid(row = 8, sticky = W, padx = 50)

    # Function Calculates Chebyshev sets Result/Error Fields
    def doCheby(self, a, b, d, func_str, x):
        d = int(d)
        c = Chebyshev(int(a), int(b), int(d), f, func_str)
        self.chebResult.set(c.eval(x))
        self.chebErr.set(f(x, func_str) / (math.pow(2, d - 1) * math.factorial(d)))
        
    def splinesWindow(self):
        # create window
        self.splines = Toplevel()
        quitBtn = Button(self.splines, text = "Submit")
        quitBtn.pack()

    def bezierWindow(self):
        # create window
        self.bezier = Toplevel()
        quitBtn = Button(self.bezier, text = "Submit")
        quitBtn.pack()
        
    def start(self):
        self.root.mainloop()

    def quitApp(self):
        self.root.destroy()

        
# create the application
gui = App()

# start the program
gui.start()
