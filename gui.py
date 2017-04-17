'''

A. Interpolation

    Chebyshev -- DONE
    Splines (cubic)
    Bezier -- DONE
    
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
import numpy as np
import bezier
import matplotlib.pyplot as plt

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
        if c.func != "err":
            eval = c.eval(x)
            if eval != "err":
                self.chebResult.set(eval)
                self.chebErr.set(f(x, func_str) / (math.pow(2, d - 1) * math.factorial(d)))
        
    def splinesWindow(self):
        # create window
        self.splines = Toplevel()
        quitBtn = Button(self.splines, text = "Submit")
        quitBtn.pack()

    def bezierWindow(self):
        # create window
        self.bezier = Toplevel()
        self.bezier.title("Bezier")
        self.bezier.resizable(0, 0)
        self.bezierEndpoints = DoubleVar()
        self.bezierControlPoints = DoubleVar()
        mainFrame = Frame(self.bezier)
        mainFrame.pack()

        # x(t) =
        Label(mainFrame, text="x(t) =").grid(row=0, column=0, sticky=W, padx=0)

        # x1:
        x1Label = Label(mainFrame, text="x1:").grid(row=1, column = 0, sticky=W)
        aBezier = Entry(mainFrame, width=3)
        aBezier.grid(row=1, column=1, sticky=W, padx=25)

        # bx:
        bxLabel = Label(mainFrame, text="bx:").grid(row=2, column=0, sticky=W)
        bBezier = Entry(mainFrame, width=3)
        bBezier.grid(row=2, column = 1, sticky=W, padx=25)

        # cx:
        cxLabel = Label(mainFrame, text="cx:").grid(row=3, column=0, sticky=W)
        cBezier = Entry(mainFrame, width=3)
        cBezier.grid(row=3, column=1, sticky=W, padx=25)

        # dx:
        dxLabel = Label(mainFrame, text="dx:").grid(row=4, column=0, sticky=W)
        dBezier = Entry(mainFrame, width=3)
        dBezier.grid(row=4, column=1, sticky=W, padx=25)

        # y(t) =
        Label(mainFrame, text="y(t) = ").grid(row=0, column=2)

        # y1:
        y1Label = Label(mainFrame, text="y1:").grid(row=1, column=2, sticky=W)
        eBezier = Entry(mainFrame, width=3)
        eBezier.grid(row=1, column=3, sticky=W, padx=25)

        # by:
        byLabel = Label(mainFrame, text="by:").grid(row=2, column=2, sticky=W)
        fBezier = Entry(mainFrame, width=3)
        fBezier.grid(row=2, column=3, sticky=W, padx=25)

        # cy:
        cyLabel = Label(mainFrame, text="cy:").grid(row=3, column=2, sticky=W)
        gBezier = Entry(mainFrame, width=3)
        gBezier.grid(row=3, column=3, sticky=W, padx=25)

        # dy:
        dyLabel = Label(mainFrame, text="dy:").grid(row=4, column=2, sticky=W)
        hBezier = Entry(mainFrame, width=3)
        hBezier.grid(row=4, column=3, sticky=W, padx=25)

        # Submit Button
        submitBtn = Button(mainFrame, text="Submit",
                           command=lambda: self.doBezier([aBezier.get(), bBezier.get(), cBezier.get(), dBezier.get(),
                                                          eBezier.get(), fBezier.get(), gBezier.get(), hBezier.get()]))
        submitBtn.grid(row=5, column=3, rowspan=2, columnspan=10, pady=10, sticky=W)

        # Endpoints
        endLabel = Label(mainFrame, text="Endpoints:").grid(row=5, column=0, sticky=W)
        endPoints = Entry(mainFrame, width=25, textvariable=self.bezierEndpoints)
        endPoints.grid(row=5, column=1, sticky=W, padx=25)

        # Control Points
        endLabel = Label(mainFrame, text="Control Points:").grid(row=6, column=0, sticky=W)
        endPoints = Entry(mainFrame, width=25, textvariable=self.bezierControlPoints)
        endPoints.grid(row=6, column=1, sticky=W, padx=25)

    def doBezier(self, vals):
        print(vals[0])
        x1 = float(vals[0])
        bx = float(vals[1])
        cx = float(vals[2])
        dx = float(vals[3])
        y1 = float(vals[4])
        by = float(vals[5])
        cy = float(vals[6])
        dy = float(vals[7])
        x2 = float((bx + 3 * x1) / 3.0)
        x3 = float((cx + 3 * x2 + bx) / 3.0)
        x4 = float(dx + x1 + bx + cx)
        y2 = float((by + 3 * y1) / 3.0)
        y3 = float((cy + 3 * y2 + by) / 3.0)
        y4 = float(dy + y1 + by + cy)

        endpoints = [[x1, y1], [x4, y4]]
        control_points =[[x2, y2], [x3, y3]]

        e1 = str(endpoints[0]).replace('[', '(')
        e1 = e1.replace(']', ')')
        e2 = str(endpoints[1]).replace('[', '(')
        e2 = e2.replace(']', ')')
        c1 = str(control_points[0]).replace('[', '(')
        c1 = c1.replace(']', ')')
        c2 = str(control_points[1]).replace('[', '(')
        c2 = c2.replace(']', ')')
        self.bezierEndpoints.set(e1 + " and " + e2)
        self.bezierControlPoints.set(c1 + " and " + c2)

        axes = {'family': 'serif', 'color': 'darkred', 'weight': 'normal', 'size': 16}
        in_graph = {'family': 'serif', 'color': 'darkred', 'weight': 'normal', 'size': 10}

        data_points_x = [x1, x2, x3, x4]
        data_points_y = [y1, y2, y3, y4]
        nodes = np.array([
            [x1, y1],
            [x2, y2],
            [x3, y3],
            [x4, x4],
        ])

        plot_min_x = min(data_points_x) - 0.25
        plot_max_x = max(data_points_x) + 0.25
        plot_min_y = min(data_points_y) - 0.25
        plot_max_y = max(data_points_y) + 0.25

        curve = bezier.Curve(nodes, degree=3)
        plot = curve.plot(num_pts=256)
        plot.axis('scaled')
        plot.set_xlim(plot_min_x, plot_max_x)
        plot.set_ylim(plot_min_y, plot_max_y)

        plt.title("Bezier Curve", fontdict=axes)
        plt.text(plot_min_x, plot_max_y - 0.25, "Endpoints: " + e1 + " and " + e2, fontdict=in_graph)
        plt.text(plot_min_x, plot_max_y - 0.5, "Control Points: " + c1 + " and " + c2, fontdict=in_graph)
        plt.show()

    def start(self):
        self.root.mainloop()

    def quitApp(self):
        self.root.destroy()

        
# create the application
gui = App()

# start the program
gui.start()
