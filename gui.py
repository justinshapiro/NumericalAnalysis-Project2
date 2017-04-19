'''

A. Interpolation

    Chebyshev -- DONE
    Splines (cubic) -- DONE
    Bezier -- DONE

B. Least Squares

    Linear
        - Classical Gram-Schmidt
        - Modified Gram-Schmidt
        - Householder Reflectors
        - QR Factorization -- DONE
    Nonlinear
        - Gauss-Newton
        - Levenberg-Marquardt

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

import matplotlib
matplotlib.use("TkAgg")
from Householder import Householder
import time
from Tkinter import *
import tkFont
from ttk import *
from chebyshev import Chebyshev
import math
from universal_function import f
import numpy as np
import bezier
import matplotlib.pyplot as plt
import scipy
from scipy import interpolate, linalg

class App(Frame):
    def __init__(self):
        self.root = Tk()
        self.root.s = Style()
        self.root.geometry("420x300")
        self.root.resizable(1,1)  # made resizable for now, may need to increase geometry
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
        self.linearBtn = Button(self.lsLabelframe, text = "Linear", width=27, command = self.linearWindow)
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

    #####################
    ### Interpolation ###
    #####################

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
        self.splines.title("Cubic Splines")
        self.splines.resizable(0, 0)
        mainFrame = Frame(self.splines)
        mainFrame.pack()
        self._font= tkFont.Font(family="Helvetica", size=8)
        self.text_box = Text(mainFrame, width=60, height=5, font=self._font)

        prompt1 = "How many data points do you have?: "
        l = Label(mainFrame, text=prompt1)
        l.grid(row=0, column=0, sticky=W, padx=0)
        aSplines = Entry(mainFrame, width=3)
        aSplines.grid(row=0, column=1, sticky=W, padx=25)

        # "Enter Points" Button
        epBtn = Button(mainFrame, text="Enter Points", command=lambda: moreSplines(int(aSplines.get())))
        epBtn.grid(row=1, column=0, pady=10, sticky=W)

        def moreSplines(n):
            l.destroy()
            aSplines.destroy()
            epBtn.destroy()

            nSplines = []
            i = 0
            row_count = 0
            while i < n:
                nSplines.append(["", ""])
                # x_i
                Label(mainFrame, text="x_" + (str(i + 1)) + ": ").grid(row=row_count, column=0, sticky=W, padx=0)
                nSplines[i][0] = Entry(mainFrame, width=3)
                nSplines[i][0].grid(row=row_count, column=0, sticky=W, padx=25)
                # y_i
                Label(mainFrame, text="y_" + (str(i + 1)) + ": ").grid(row=row_count, column=1, sticky=W, padx=0)
                nSplines[i][1] = Entry(mainFrame, width=3)
                nSplines[i][1].grid(row=row_count, column=1, sticky=W, padx=25)
                row_count += 1
                i += 1

            _l = Label(mainFrame, text="Spline Equations: ")

            # Submit Button
            submitBtn = Button(mainFrame, text="Submit", command=lambda: self.doSplines(nSplines))
            submitBtn.grid(row=row_count, column=0, columnspan=3, pady=10, sticky=W)
            row_count += 1

            _l.grid(row=row_count, column=0, sticky=W, padx=0)
            row_count += 1
            self.text_box.grid(row=row_count, column=0, columnspan=4, sticky=W)

    def doSplines(self, nSplines):
        i = 0
        all_points = []
        while i < len(nSplines):
            all_points.append(["", ""])
            all_points[i][0] = nSplines[i][0].get()
            all_points[i][1] = nSplines[i][1].get()
            i += 1

        # assert that points are sorted by increasing x value
        all_points = sorted(all_points, key=lambda x: (x[0]))

        x = []
        i = 0
        while i < len(all_points):
            x.append(float(all_points[i][0]))
            i += 1
        y = []
        i = 0
        while i < len(all_points):
            y.append(float(all_points[i][1]))
            i += 1

        x_np = np.array(x)
        y_np = np.array(y)
        arr = np.arange(np.amin(x), np.amax(x), 0.01)
        s = interpolate.CubicSpline(x_np, y_np, bc_type=((2, 0.0), (2, 0.0)))

        s_arr = []
        i = 0
        while i < len(s.c) - 1:
            inner_sign = ""
            if x[i] < 0:
                inner_sign = "+ "
            else:
                inner_sign = "- "
            s_str = "S_" + str(i + 1) + "(x) = "
            s_str += str(s.c[3, i])
            if float(s.c[2, i]) < 0:
                s_str += " - "
            else:
                s_str += " + "
            s_str += str(abs(s.c[2, i])) + "(x "
            s_str += inner_sign + str(x[i]) + ") "
            if float(s.c[1, i]) < 0:
                s_str += "- "
            else:
                s_str += "+ "
            s_str += str(abs(s.c[1, i])) + "(x "
            s_str += inner_sign + str(x[i]) + ")^2 "
            if float(s.c[0, i]) < 0:
                s_str += "- "
            else:
                s_str += "+ "
            s_str += str(abs(s.c[0, i])) + "(x "
            s_str += inner_sign + str(x[i]) + ")^3"
            s_arr.append(s_str)
            i += 1

        i = 0
        spline_eqs = ""
        while i < len(s_arr):
            spline_eqs += str(s_arr[i]) + "\n"
            i += 1

        print(spline_eqs)
        self.text_box.insert(END, spline_eqs)

        plt.plot(x_np, y_np, 'bo', label='Data Point')
        plt.plot(arr, s(arr), 'r-', label='Cubic Spline')
        plt.legend()
        plt.show()

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

    #####################
    ### Least Squares ###
    #####################

    def linearWindow(self):
        # create window
        linear = Toplevel(self)
        linear.title("Linear Least Squares")
        linear.resizable(0, 0)
        mainFrame = Frame(linear)
        mainFrame.pack()

        Button(mainFrame, text = "Classical Gram-Schmidt", command = lambda: cGramSchmidtWindow()).pack(fill = X)
        Button(mainFrame, text = "Modified Gram-Schmidt", command = lambda: modifiedGSWindow()).pack(fill = X)
        Button(mainFrame, text = "Householder Reflectors", command = lambda: householderWindow()).pack(fill = X)
        Button(mainFrame, text = "QR Factorization", command = lambda: qrWindow()).pack(fill = X)
        Button(mainFrame, text = "Exit Window", command = lambda: linear.destroy()).pack(fill = X)

        def cGramSchmidtWindow():
            #create window
            classical = Toplevel()
            classical.title("Classical Gram-Schmidt")
            mainFrame = Frame(classical)
            mainFrame.pack(fill = "both")

            Button(mainFrame, text = "Exit Window", command = lambda: classical.destroy()).pack(fill = X)

        def modifiedGSWindow():
            #create window
            modified = Toplevel()
            modified.title("Modified Gram-Schmidt")
            modified.resizable(0,0)
            mainFrame = Frame(modified)
            mainFrame.pack()

            Button(mainFrame, text = "Exit Window", command = lambda: modified.destroy()).pack(fill = X)

        def householderWindow():
            # create window
            householder = Toplevel()
            householder.title("Householder")
            mainFrame = Frame(householder)
            mainFrame.pack(fill="both")

            l = Label(mainFrame, text="Enter size of matrix A? (n x m)")
            l.grid(row=0, column=0, sticky=W, padx=0)
            rowA = Entry(mainFrame, width=4)
            rowA.grid(row=0, column=1, sticky=W, padx=10)
            l2 = Label(mainFrame, text="x")
            l2.grid(row=0, column=2, sticky=W)
            colA = Entry(mainFrame, width=4)
            colA.grid(row=0, column=3, sticky=W, padx=15)

            # "Submit" Button
            sBtn = Button(mainFrame, text="Submit", command=lambda: continueHouseholder(int(rowA.get()), int(colA.get())))
            sBtn.grid(row=1, column=0, pady=10, sticky=W)

            def continueHouseholder(row, col):
                l.destroy()
                l2.destroy()
                rowA.destroy()
                colA.destroy()
                sBtn.destroy()

                A = []
                i = 0
                rowCount = 1

                Label(mainFrame, text = "A =").grid(row = 0, column = 0, sticky = W)
                # 3 x 3
                while i < row:
                    A.append([""] * col)
                    j = 0

                    # Print each row entry
                    while j < col:
                        A[i][j] = Entry(mainFrame, width = 3)
                        A[i][j].grid(row = rowCount, column = j, sticky = W, padx = 5)
                        j += 1

                    i += 1
                    rowCount += 1

                # Submit Button
                submitBtn = Button(householder, text="Submit", command=lambda: doHouseholder(A, row, col))
                submitBtn.pack(fill = "both")
                rowCount += 2

                resultFrame = Frame(householder)
                resultFrame.pack(fill = "x")

                scrollbar = Scrollbar(resultFrame)
                scrollbar.pack(side=RIGHT, fill=Y)

                self.householderTextBox = Text(resultFrame)
                self.householderTextBox.pack(fill = "both")
                self.householderTextBox.config(yscrollcommand = scrollbar.set)
                scrollbar.config(command = self.householderTextBox.yview)

                Button(householder, text = "Exit Window", command = lambda: householder.destroy()).pack(side = BOTTOM, fill = "both")

                def doHouseholder(inputA, r, c):
                    i = 0
                    ourMatrix = []
                    while i < len(inputA):
                        ourMatrix.append([""] * c)
                        j = 0

                        while j < c:
                            ourMatrix[i][j] = float(inputA[i][j].get())
                            j += 1

                        i += 1

                    A = scipy.array(ourMatrix)  # test values, also tested 3 by 3
                    h = Householder()
                    Q, R = h.householder(A)

                    self.householderTextBox.insert(END, "A:\n")
                    for row in np.matrix(ourMatrix):
                        self.householderTextBox.insert(END, str(row) + '\n')

                    self.householderTextBox.insert(END, "Q:\n")
                    for row in Q:
                        self.householderTextBox.insert(END, str(row) + '\n')

                    self.householderTextBox.insert(END, "R:\n")
                    for row in R:
                        self.householderTextBox.insert(END, str(row) + '\n')

        def qrWindow():
            #create window
            qr = Toplevel()
            qr.title("QR Factorization")
            mainFrame = Frame(qr)
            mainFrame.pack(fill = "both")

            l = Label(mainFrame, text = "Enter size of matrix A? (n x m)")
            l.grid(row=0, column=0, sticky=W, padx=0)
            rowA = Entry(mainFrame, width = 4)
            rowA.grid(row=0, column=1, sticky=W, padx=10)
            l2 = Label(mainFrame, text = "x")
            l2.grid(row = 0, column = 2, sticky = W)
            colA = Entry(mainFrame, width = 4)
            colA.grid(row = 0, column = 3, sticky = W, padx = 15)

            # "Submit" Button
            sBtn = Button(mainFrame, text="Submit", command=lambda: continueQr(int(rowA.get()), int(colA.get())))
            sBtn.grid(row=1, column=0, pady=10, sticky=W)

            def continueQr(row, col):
                l.destroy()
                l2.destroy()
                rowA.destroy()
                colA.destroy()
                sBtn.destroy()

                A = []
                i = 0
                rowCount = 1

                Label(mainFrame, text = "A =").grid(row = 0, column = 0, sticky = W)
                # 3 x 3
                while i < row:
                    A.append([""] * col)
                    j = 0

                    # Print each row entry
                    while j < col:
                        A[i][j] = Entry(mainFrame, width = 3)
                        A[i][j].grid(row = rowCount, column = j, sticky = W, padx = 5)
                        j += 1

                    i += 1
                    rowCount += 1

                # Submit Button
                submitBtn = Button(qr, text="Submit", command = lambda: doQr(A, row, col))
                submitBtn.pack(fill = "both")
                rowCount += 2

                resultFrame = Frame(qr)
                resultFrame.pack(fill = "x")

                scrollbar = Scrollbar(resultFrame)
                scrollbar.pack(side=RIGHT, fill=Y)

                self.qrTextBox = Text(resultFrame)
                self.qrTextBox.pack(fill = "both")
                self.qrTextBox.config(yscrollcommand = scrollbar.set)
                scrollbar.config(command = self.qrTextBox.yview)

                Button(qr, text = "Exit Window", command = lambda: qr.destroy()).pack(side = BOTTOM, fill = "both")

                def doQr(inputA, r, c):
                    i = 0
                    ourMatrix = []
                    while i < len(inputA):
                        ourMatrix.append([""] * c)
                        j = 0

                        while j < c:
                            ourMatrix[i][j] = inputA[i][j].get()
                            j += 1

                        i += 1

                    A = scipy.array(ourMatrix)  # test values, also tested 3 by 3
                    Q, R = scipy.linalg.qr(A)

                    self.qrTextBox.insert(END, "A:\n")
                    for row in np.matrix(ourMatrix):
                        self.qrTextBox.insert(END, str(row) + '\n')

                    self.qrTextBox.insert(END, "Q:\n")
                    for row in Q:
                        self.qrTextBox.insert(END, str(row) + '\n')

                    self.qrTextBox.insert(END, "R:\n")
                    for row in R:
                        self.qrTextBox.insert(END, str(row) + '\n')

    def nonLinearWindow(self):
        print "hi"

    def start(self):
        self.root.mainloop()

    def quitApp(self):
        self.root.destroy()


# create the application
gui = App()

# start the program
gui.start()
