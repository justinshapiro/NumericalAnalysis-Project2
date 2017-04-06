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
        # create window
        self.cheby = Toplevel()
        quitBtn = Button(self.cheby, text = "Submit")
        quitBtn.pack()

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
