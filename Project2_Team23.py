from Tkinter import *
import tkFont
from ttk import *
import matplotlib
import timeit
import matplotlib.backends.backend_tkagg
matplotlib.use("TkAgg") # needed for Macs
from Householder import Householder
import time
from chebyshev import Chebyshev
import math
from universal_function import *
import numpy as np
import FileDialog
import bezier
import matplotlib.pyplot as plt
import scipy
from scipy import interpolate, linalg
from scipy.interpolate import lagrange
from NDD import *
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from scipy.integrate import quad, quadrature
from sympy.utilities.lambdify import lambdify
from ad_forward import *
from ad import adnumber
from NewtonCodes import *

class App(Frame):
    def __init__(self):
        self.root = Tk()
        self.root.s = Style()
        self.root.geometry("420x300")
        self.root.resizable(1, 1)  # made resizable for now, may need to increase geometry
        self.root.s.theme_use("vista")
        self.root.title("Numerical Analysis - Project 2")

        Frame.__init__(self, self.root)
        self.createWidgets()

    def wait(self):
        while not w.can_make_request():
            time.sleep(1)

    def createWidgets(self):
        # Interpolation Frame
        self.interpLabelframe = LabelFrame(self.root, text = "Interpolation", labelanchor='n')
        self.interpLabelframe.grid(row = 0, columnspan = 7, sticky = 'WE', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.interpLabelframe.pack(fill = 'both', expand = 'yes')
        self.innerInFrame = Frame(self.interpLabelframe)
        self.innerInFrame.grid(padx=1)

        # Interpolation Frame Buttons
        self.lagrangeButton = Button(self.innerInFrame, text="Lagrange", width=20, command=self.lagrangeWindow)
        self.nddButton = Button(self.innerInFrame, text="Newton's Divided Diff", width=20, command=self.nddWindow)
        self.chebyButton = Button(self.innerInFrame, text = "Chebyshev", width=20, command = self.chebyWindow)
        self.splinesButton = Button(self.innerInFrame, text = "Cubic Splines", width=20, command = self.splinesWindow)
        self.bezierButton = Button(self.innerInFrame, text = "Bezier", width=21, command = self.bezierWindow)
        self.lagrangeButton.grid(row=0, column=0)
        self.nddButton.grid(row=0, column=1)
        self.chebyButton.grid(row=0, column=2)
        self.splinesButton.grid(row=1, column=0, columnspan=2)
        self.bezierButton.grid(row=1, column=1, columnspan=2)

        # Least Squares Frame
        self.lsLabelframe = LabelFrame(self.root, text = "Least Squares", labelanchor='n')
        self.lsLabelframe.grid(row = 2, sticky = 'WE', \
                               padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.lsLabelframe.pack(fill = 'both', expand = 'yes')
        self.innerLsFrame = Frame(self.lsLabelframe)
        self.innerLsFrame.grid(padx = 118)

        # Least Squares Frame Buttons
        self.linearBtn = Button(self.lsLabelframe, text = "Linear", width=27, command = self.linearWindow)
        self.nonLinBtn = Button(self.lsLabelframe, text = "Nonlinear", width=27, command = self.nonLinearWindow)
        self.linearBtn.grid(row = 0, column = 0, sticky = W)
        self.nonLinBtn.grid(row = 0, column = 1)

        # Differentiation and Integration Frame
        self.diffAndInt = Frame(self.root)
        self.diffAndInt.grid(row = 0, columnspan = 7, sticky = 'WE', padx = 5, pady = 5, ipadx = 10, ipady = 5)
        self.diffAndInt.pack(fill = 'both', expand = 'yes')

        # Sub Frames
        self.diffFrame = LabelFrame(self.diffAndInt, text = "Differentiation", labelanchor='n')
        self.intFrame = LabelFrame(self.diffAndInt, text = "Integration", labelanchor='n')
        self.diffFrame.grid(row = 0, column = 0, columnspan = 2)
        self.intFrame.grid(row = 1, column = 0)
        self.diffFrame.pack(expand = 'yes')
        self.intFrame.pack(expand = 'yes')

        # Differentiation and Integration Buttons
        self.differenceBtn = Button(self.diffFrame, text = "Difference Methods", command = self.diffMethodsWindow)
        self.extrapBtn = Button(self.diffFrame, text = "Extrapolation", width=20, command = self.extrapWindow)
        self.autoDiffBtn = Button(self.diffFrame, text = "Automatic Differentiation", command = self.adWindow)
        self.newtonCodesBtn = Button(self.intFrame, text = "Newton-Cotes", width=20, command = self.nCodesWindow)
        self.rombergBtn = Button(self.intFrame, text = "Romberg", width=20, command = self.rombergWindow)
        self.adaptBtn = Button(self.intFrame, text = "Quadrature", width=20, command = self.quadraWindow)
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

    def lagrangeWindow(self):
        self.lagrange = Toplevel()
        self.lagrange.title("Lagrange")
        self.lagrange.resizable(0,0)
        mainFrame = Frame(self.lagrange)
        self._font = tkFont.Font(family="Helvetica", size=8)
        self.text_box = Text(mainFrame, width=60, height=5, font=self._font)
        mainFrame.pack()

        prompt1 = "How many data points do you have?: "
        l = Label(mainFrame, text=prompt1)
        l.grid(row=0, column=0, sticky=W, padx=0)
        aLagrange = Entry(mainFrame, width=3)
        aLagrange.grid(row=0, column=1, sticky=W, padx=25)

        # "Enter Points" Button
        epBtn = Button(mainFrame, text="Enter Points", command=lambda: moreLagrange(int(aLagrange.get())))
        epBtn.grid(row=1, column=0, pady=10, sticky=W)

        def moreLagrange(n):
            l.destroy()
            aLagrange.destroy()
            epBtn.destroy()

            points = []
            i = 0
            row_count = 0
            while i < n:
                points.append(["", ""])
                # x_i
                Label(mainFrame, text="x_" + (str(i + 1)) + ": ").grid(row=row_count, column=0, sticky=W, padx=0)
                points[i][0] = Entry(mainFrame, width=3)
                points[i][0].grid(row=row_count, column=0, sticky=W, padx=25)
                # y_i
                Label(mainFrame, text="y_" + (str(i + 1)) + ": ").grid(row=row_count, column=1, sticky=W, padx=0)
                points[i][1] = Entry(mainFrame, width=3)
                points[i][1].grid(row=row_count, column=1, sticky=W, padx=25)
                row_count += 1
                i += 1

            _l = Label(mainFrame, text="Interpolating Polynomial: ")

            # Submit Button
            submitBtn = Button(mainFrame, text="Submit", command=lambda: self.doLagrange(points))
            submitBtn.grid(row=row_count, column=0, columnspan=3, pady=10, sticky=W)
            row_count += 1

            _l.grid(row=row_count, column=0, sticky=W, padx=0)
            row_count += 1
            self.text_box.grid(row=row_count, column=0, columnspan=4, sticky=W)

    def doLagrange(self, points):
        x = []
        y = []
        i = 0
        while i < len(points):
            x.append(float(points[i][0].get()))
            y.append(float(points[i][1].get()))
            i += 1

        start_time = timeit.default_timer()
        P = str(lagrange(x, y))
        end_time = timeit.default_timer() - start_time

        if P.find("inf") > -1 or P.find("nan") > -1:
            self.text_box.insert(END, "Error: Points yield division by zero. Check your input")
        else:
            i = 0
            exp_list = []
            while P[i] != '\n':
                if P[i].isdigit():
                    exp_list.append(P[i])
                i += 1
            P = P.split('\n')[1]
            i = 0
            while i < len(P) and len(exp_list) > 0:
                if P[i] == 'x':
                    P = P[:i + 1] + "^" + str(exp_list.pop()) + P[i + 1:]
                i += 1
            P = P.replace(' ', '')
            self.text_box.insert(END, "P(x) = " + P + "\n")
            self.text_box.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def nddWindow(self):
        self.ndd = Toplevel()
        self.ndd.title("Newton's Divided Differences")
        self.ndd.resizable(0,0)
        mainFrame = Frame(self.ndd)
        self._font = tkFont.Font(family="Helvetica", size=8)
        self.text_box = Text(mainFrame, width=60, height=5, font=self._font)
        mainFrame.pack()

        prompt1 = "How many data points do you have?: "
        l = Label(mainFrame, text=prompt1)
        l.grid(row=0, column=0, sticky=W, padx=0)
        aNDD = Entry(mainFrame, width=3)
        aNDD.grid(row=0, column=1, sticky=W, padx=25)

        # "Enter Points" Button
        epBtn = Button(mainFrame, text="Enter Points", command=lambda: moreNDD(int(aNDD.get())))
        epBtn.grid(row=1, column=0, pady=10, sticky=W)

        def moreNDD(n):
            l.destroy()
            aNDD.destroy()
            epBtn.destroy()

            points = []
            i = 0
            row_count = 0
            while i < n:
                points.append(["", ""])
                # x_i
                Label(mainFrame, text="x_" + (str(i + 1)) + ": ").grid(row=row_count, column=0, sticky=W, padx=0)
                points[i][0] = Entry(mainFrame, width=3)
                points[i][0].grid(row=row_count, column=0, sticky=W, padx=25)

                # y_i
                Label(mainFrame, text="y_" + (str(i + 1)) + ": ").grid(row=row_count, column=1, sticky=W, padx=0)
                points[i][1] = Entry(mainFrame, width=3)
                points[i][1].grid(row=row_count, column=1, sticky=W, padx=25)
                row_count += 1
                i += 1

            _l = Label(mainFrame, text="Interpolating Polynomial: ")

            # Submit Button
            submitBtn = Button(mainFrame, text="Submit", command=lambda: self.doNDD(points))
            submitBtn.grid(row=row_count, column=0, columnspan=3, pady=10, sticky=W)
            row_count += 1

            _l.grid(row=row_count, column=0, sticky=W, padx=0)
            row_count += 1
            self.text_box.grid(row=row_count, column=0, columnspan=4, sticky=W)

    def doNDD(self, points):
        start_time = timeit.default_timer()
        x = []
        y = []
        i = 0
        while i < len(points):
            x.append(float(points[i][0].get()))
            y.append(float(points[i][1].get()))
            i += 1

        coefs = list(newtdd(x, y))
        if str(coefs).find("inf") > -1 or str(coefs).find("nan") > -1:
            self.text_box.insert(END, "Error: Points yield division by zero. Check your input")
        else:
            exponent = len(coefs) - 1
            P = ""
            i = 0
            while len(coefs) > 0:
                if i > 0:
                    P += "%+f" % coefs.pop()
                else:
                    P += "%f" % coefs.pop()
                if len(coefs) > 0:
                    P += "x"
                    if len(coefs) > 1:
                        P += "^" + str(exponent)
                        exponent -= 1
                i += 1

            end_time = timeit.default_timer() - start_time
            self.text_box.insert(END, "P(x) = " + P + "\n")
            self.text_box.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def chebyWindow(self):
        # create Chebyshev window
        self.cheby = Toplevel()
        self.cheby.title("Chebyshev")
        self.cheby.resizable(0,0)
        self.chebResult = DoubleVar()
        self.chebErr = DoubleVar()
        self.chebsecutionTime = DoubleVar()
        mainFrame = Frame(self.cheby)
        mainFrame.pack()

        # Interval Label
        Label(mainFrame, text = "Enter Interval [a, b] \n(where a <= x <= b):").grid(row = 0, sticky = W)

        # a label and entry box
        aLabel = Label(mainFrame, text = "a:").grid(row = 1, sticky = W)
        aCheb = Entry(mainFrame, width = 5)
        aCheb.grid(row = 1, sticky = W, padx = 50)

        # b label and entry box
        bLabel = Label(mainFrame, text = "b:").grid(row = 2, sticky = W)
        bCheb = Entry(mainFrame, width = 5)
        bCheb.grid(row = 2, sticky = W, padx = 50)

        # degree label and entry box
        dLabel = Label(mainFrame, text = "Degree:").grid(row = 3, sticky = W)
        dCheb = Entry(mainFrame, width = 5)
        dCheb.grid(row = 3, sticky = W, padx = 50)

        # f(x) label and entry box
        fLabel = Label(mainFrame, text = "f(x):").grid(row = 4, sticky = W)
        fCheb = Entry(mainFrame, width = 15)
        fCheb.grid(row = 4, sticky = W, padx = 50)

        # x label and entry box
        xLabel = Label(mainFrame, text="x = ").grid(row=5, sticky=W)
        xCheb = Entry(mainFrame, width=5)
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

        # Execution time box
        Label(mainFrame, text="Execution time: ").grid(row=9, sticky=W)
        errMsg = Entry(mainFrame, width=40, textvariable=self.chebsecutionTime)
        errMsg.grid(row=10, sticky=W, padx=50)

    # Function Calculates Chebyshev sets Result/Error Fields
    def doCheby(self, a, b, d, func_str, x):
        start_time = timeit.default_timer()
        d = int(d)
        try:
            assert (int(d) <= 150)
            try:
                assert (float(a) <= float(x) and float(x) <= float(b))
                c = Chebyshev(int(a), int(b), d, f, func_str)
                if c.func != "err":
                    eval = c.eval(x)
                    end_time = timeit.default_timer() - start_time
                    if eval != "err":
                        self.chebResult.set(eval)
                        self.chebErr.set(f(x, func_str) / (math.pow(2, int(d) - 1) * math.factorial(d)))
                        self.chebsecutionTime.set(str(end_time) + " seconds\n")
            except AssertionError:
                self.chebResult.set("Error: x doesn't meet the requirement a <= x <= b")
        except AssertionError:
            self.chebResult.set("Error: Degree is too large, must be less than or equal to 150")

    def splinesWindow(self):
        # create window
        self.splines = Toplevel()
        self.splines.title("Cubic Splines")
        self.splines.resizable(1, 1)
        mainFrame = Frame(self.splines)
        mainFrame.pack()
        self._font = tkFont.Font(family="Helvetica", size=8)
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
        last_x = "null"
        err = False
        i = 0
        while i < len(all_points):
            if last_x == "null":
                last_x = all_points[i][0]
            else:
                if all_points[i][0] == last_x:
                    err = True
                    break
                else:
                    last_x = all_points[i][0]
            i += 1

        if not err:
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
            start_time = timeit.default_timer()
            s = scipy.interpolate.CubicSpline(x_np, y_np, bc_type=((2, 0.0), (2, 0.0)))
            end_time = timeit.default_timer() - start_time

            s_arr = []
            i = 0
            while i < len(s.c[1]):
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

            self.text_box.insert(END, spline_eqs)
            self.text_box.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

            plt.plot(x_np, y_np, 'bo', label='Data Point')
            plt.plot(arr, s(arr), 'r-', label='Cubic Spline')
            plt.legend()
            plt.show()
        else:
            self.text_box.insert(END, "Error: x must be a strictly increasing sequence (no duplicate x-values allowed)")

    def bezierWindow(self):
        # create window
        self.bezier = Toplevel()
        self.bezier.title("Bezier")
        self.bezier.resizable(0, 0)
        self.bezierEndpoints = DoubleVar()
        self.bezierControlPoints = DoubleVar()
        self.bezicutionTime = DoubleVar()
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

        # Execution Time
        endLabel = Label(mainFrame, text="Execution Time:").grid(row=7, column=0, sticky=W)
        endPoints = Entry(mainFrame, width=25, textvariable=self.bezicutionTime)
        endPoints.grid(row=7, column=1, sticky=W, padx=25)

    def doBezier(self, vals):
        x1 = float(vals[0])
        bx = float(vals[1])
        cx = float(vals[2])
        dx = float(vals[3])
        y1 = float(vals[4])
        by = float(vals[5])
        cy = float(vals[6])
        dy = float(vals[7])
        start_time = timeit.default_timer()
        x2 = float((bx + 3 * x1) / 3.0)
        x3 = float((cx + 3 * x2 + bx) / 3.0)
        x4 = float(dx + x1 + bx + cx)
        y2 = float((by + 3 * y1) / 3.0)
        y3 = float((cy + 3 * y2 + by) / 3.0)
        y4 = float(dy + y1 + by + cy)

        endpoints = [[x1, y1], [x4, y4]]
        control_points =[[x2, y2], [x3, y3]]

        end_time = timeit.default_timer() - start_time
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
        self.bezicutionTime.set(str(end_time) + " seconds\n")

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

        Button(mainFrame, text = "Solve via Linear Least Squares", command = lambda: lsWindow()).pack(fill = X)
        Button(mainFrame, text="QR Factorization via Gram-Schmidt", command=lambda: qrWindow()).pack(fill=X)
        Button(mainFrame, text = "QR via Householder Reflectors", command = lambda: householderWindow()).pack(fill = X)
        Button(mainFrame, text = "Exit Window", command = lambda: linear.destroy()).pack(fill = X)

        def lsWindow():
            # create window
            ls = Toplevel()
            ls.title("Solve via Linear Least Squares")
            mainFrame = Frame(ls)
            mainFrame.pack(fill="both")

            l = Label(mainFrame, text="Enter size of matrix A? (n x m)")
            l.grid(row=0, column=0, sticky=W, padx=0)
            rowA = Entry(mainFrame, width=4)
            rowA.grid(row=0, column=1, sticky=W, padx=10)
            l2 = Label(mainFrame, text="x")
            l2.grid(row=0, column=2, sticky=W)
            colA = Entry(mainFrame, width=4)
            colA.grid(row=0, column=3, sticky=W, padx=15)

            l3 = Label(mainFrame, text="Enter size of matrix B? (n x 1)")
            l3.grid(row=1, column=0, sticky=W, padx=0)
            rowB = Entry(mainFrame, width=4)
            rowB.grid(row=1, column=1, sticky=W, padx=10)
            l4 = Label(mainFrame, text="x")
            l4.grid(row=1, column=2, sticky=W, padx=0)
            colB = Entry(mainFrame, width=4)
            colB.grid(row=1, column=3, sticky=W, padx=10)
            colB.insert(0, "1")
            colB.config(state='disabled')

            # "Submit" Button
            sBtn = Button(mainFrame, text="Submit", command=lambda: continueLS(int(rowA.get()), int(colA.get()), int(rowB.get())))
            sBtn.grid(row=2, column=0, pady=10, sticky=W)

            def continueLS(row_A, col_A, row_B):
                l.destroy()
                l2.destroy()
                l3.destroy()
                l4.destroy()
                rowA.destroy()
                rowB.destroy()
                colA.destroy()
                colB.destroy()
                sBtn.destroy()

                A = []
                i = 0
                j = 0
                rowCount = 1

                Label(mainFrame, text="A =").grid(row=0, column=0, sticky=W)
                while i < row_A:
                    A.append([""] * col_A)
                    j = 0

                    # Print each row entry
                    while j < col_A:
                        A[i][j] = Entry(mainFrame, width=3)
                        A[i][j].grid(row=rowCount, column=j, sticky=W, padx=5)
                        j += 1

                    i += 1
                    rowCount += 1

                B = []
                i = 0
                k = j + 1
                rowCount = 1

                Label(mainFrame, text="B =").grid(row=0, column=k, sticky=W)
                k += 1
                while i < row_B:
                    B.append([""])
                    B[i] = Entry(mainFrame, width=3)
                    B[i].grid(row=rowCount, column=k, sticky=W, padx=5)

                    i += 1
                    rowCount += 1

                # Submit Button
                submitBtn = Button(ls, text="Submit", command=lambda: doLeastSquares(A, B, col_A))
                submitBtn.pack(fill="both")

                resultFrame = Frame(ls)
                resultFrame.pack(fill="x")

                scrollbar = Scrollbar(resultFrame)
                scrollbar.pack(side=RIGHT, fill=Y)

                self.lsTextBox = Text(resultFrame)
                self.lsTextBox.pack(fill="both")
                self.lsTextBox.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=self.lsTextBox.yview)

                Button(ls, text="Exit Window", command=lambda: ls.destroy()).pack(fill=X)

                def doLeastSquares(A, B, col):
                    i = 0
                    matrix_A = []
                    while i < len(A):
                        matrix_A.append([""] * col)
                        j = 0
                        while j < col:
                            matrix_A[i][j] = float(A[i][j].get())
                            j += 1
                        i += 1

                    i = 0
                    matrix_B = []
                    while i < len(B):
                        matrix_B.append([""])
                        matrix_B[i] = float(B[i].get())
                        i += 1

                    start_time = timeit.default_timer()
                    X = np.linalg.lstsq(matrix_A, matrix_B)
                    residual = matrix_B - np.matmul(matrix_A, X[0])
                    inner_square = 0
                    for r in residual:
                        inner_square += float(r)**2
                    rmse = math.sqrt(inner_square / len(residual))
                    end_time = timeit.default_timer() - start_time

                    self.lsTextBox.insert(END, "X: ")
                    self.lsTextBox.insert(END, str(X[0]) + '^T\n')
                    self.lsTextBox.insert(END, "RMSE: " + str(rmse) + "\n")
                    self.lsTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n\n")

        def qrWindow():
            # create window
            qr = Toplevel()
            qr.title("QR Factorization via Gram-Schmidt")
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
                submitBtn = Button(qr, text="Submit", command = lambda: doQr(A, col))
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

                def doQr(inputA, c):
                    i = 0
                    ourMatrix = []
                    while i < len(inputA):
                        ourMatrix.append([""] * c)
                        j = 0

                        while j < c:
                            ourMatrix[i][j] = inputA[i][j].get()
                            j += 1
                        i += 1

                    start_time = timeit.default_timer()
                    A = scipy.array(ourMatrix)
                    Q, R = scipy.linalg.qr(A)
                    end_time = timeit.default_timer() - start_time

                    self.qrTextBox.insert(END, "A:\n")
                    for row in np.matrix(ourMatrix):
                        self.qrTextBox.insert(END, str(row) + '\n')

                    self.qrTextBox.insert(END, "Q:\n")
                    for row in Q:
                        self.qrTextBox.insert(END, str(row) + '\n')

                    self.qrTextBox.insert(END, "R:\n")
                    for row in R:
                        self.qrTextBox.insert(END, str(row) + '\n')
                    self.qrTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

        def householderWindow():
            # create window
            householder = Toplevel()
            householder.title("QR via Householder Reflectors")
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

                    start_time = timeit.default_timer()
                    A = scipy.array(ourMatrix)  # test values, also tested 3 by 3
                    h = Householder()
                    Q, R = h.householder(A)
                    end_time = timeit.default_timer() - start_time

                    self.householderTextBox.insert(END, "A:\n")
                    for row in np.matrix(ourMatrix):
                        self.householderTextBox.insert(END, str(row) + '\n')

                    self.householderTextBox.insert(END, "Q:\n")
                    for row in Q:
                        self.householderTextBox.insert(END, str(row) + '\n')

                    self.householderTextBox.insert(END, "R:\n")
                    for row in R:
                        self.householderTextBox.insert(END, str(row) + '\n')
                    self.householderTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def nonLinearWindow(self):
        # create window
        nonlinear = Toplevel(self)
        nonlinear.title("Linear Least Squares")
        nonlinear.resizable(0, 0)
        mainFrame = Frame(nonlinear)
        mainFrame.pack()

        Button(mainFrame, text="Gauss-Newton", command=lambda: gnWindow(0)).pack(fill=X)
        Button(mainFrame, text="Levenberg-Marquardt", command=lambda: gnWindow(1)).pack(fill=X)
        Button(mainFrame, text="Exit Window", command=lambda: nonlinear.destroy()).pack(fill=X)

        def gnWindow(_type):
            # create window
            self.gn = Toplevel()
            if _type == 0:
                self.gn.title("Gauss-Newton Method")
            elif _type == 1:
                self.gn.title("Levenberg-Marquardt Method")
            mainFrame = Frame(self.gn)
            mainFrame.pack(fill = "both")

            prompt1 = "How many data points do you have?: "
            l = Label(mainFrame, text=prompt1)
            l.grid(row=0, column=0, sticky=W, padx=0)
            aGN = Entry(mainFrame, width=3)
            aGN.grid(row=0, column=1, sticky=W, padx=25)

            # "Enter Points" Button
            epBtn = Button(mainFrame, text="Enter Points", command=lambda: moreGN(int(aGN.get())))
            epBtn.grid(row=1, column=0, pady=10, sticky=W)

            def moreGN(n):
                l.destroy()
                aGN.destroy()
                epBtn.destroy()

                row_count = 0

                Label(mainFrame, text="Enter points:").grid(row=row_count, column=0, sticky=W, padx=0)
                row_count += 1

                points = []
                i = 0
                while i < n:
                    points.append(["", ""])
                    # x_i
                    Label(mainFrame, text="x_" + (str(i + 1)) + ": ").grid(row=row_count, column=0, sticky=W, padx=0)
                    points[i][0] = Entry(mainFrame, width=3)
                    points[i][0].grid(row=row_count, column=0, sticky=W, padx=25)
                    # y_i
                    Label(mainFrame, text="y_" + (str(i + 1)) + ": ").grid(row=row_count, column=1, sticky=W, padx=0)
                    points[i][1] = Entry(mainFrame, width=3)
                    points[i][1].grid(row=row_count, column=1, sticky=W, padx=25)
                    row_count += 1
                    i += 1

                Label(mainFrame, text="Enter radii:").grid(row=row_count, column=0, sticky=W, padx=0)
                row_count += 1

                R = []
                i = 0
                while i <= len(points[0]):
                    # R_i
                    R.append("")
                    Label(mainFrame, text="R_" + (str(i + 1)) + ": ").grid(row=row_count, column=0, sticky=W, padx=0)
                    R[i] = Entry(mainFrame, width=3)
                    R[i].grid(row=row_count, column=0, sticky=W, padx=25)
                    row_count += 1
                    i += 1

                vk = []
                Label(mainFrame, text="Enter the starting vector:").grid(row=row_count, column=0, sticky=W, padx=0)
                row_count += 1
                vk.append("")
                Label(mainFrame, text="x^0: ").grid(row=row_count, column=0, sticky=W, padx=0)
                vk[0] = Entry(mainFrame, width=3)
                vk[0].grid(row=row_count, column=0, sticky=W, padx=25)
                row_count += 1
                vk.append("")
                Label(mainFrame, text="y^0: ").grid(row=row_count, column=0, sticky=W, padx=0)
                vk[1] = Entry(mainFrame, width=3)
                vk[1].grid(row=row_count, column=0, sticky=W, padx=25)
                row_count += 1

                k = "null"
                Label(mainFrame, text="If you have a K value, enter here (optional):").grid(row=row_count, column=0, sticky=W, padx=0)
                k = Entry(mainFrame, width=3)
                k.grid(row=row_count, column=1, sticky=W, padx=25)
                row_count += 1

                _lambda = 0
                if _type == 1:
                    Label(mainFrame, text="Lambda:").grid(row=row_count, column=0, sticky=W, padx=0)
                    _lambda = Entry(mainFrame, width=3)
                    _lambda.grid(row=row_count, column=1, sticky=W, padx=25)
                    row_count += 1

                it = 0
                Label(mainFrame, text="Enter number of iterations:").grid(row=row_count, column=0, sticky=W, padx=0)
                it = Entry(mainFrame, width=3)
                it.grid(row=row_count, column=1, sticky=W, padx=25)
                row_count += 1

                # Submit Button
                submitBtn = Button(self.gn, text="Submit", command=lambda: doGN(points, R, vk, k, _lambda, it))
                submitBtn.pack(fill="both")
                row_count += 2

                resultFrame = Frame(self.gn)
                resultFrame.pack(fill="x")

                scrollbar = Scrollbar(resultFrame)
                scrollbar.pack(side=RIGHT, fill=Y)

                self.gnTextBox = Text(resultFrame)
                self.gnTextBox.pack(fill="both")
                self.gnTextBox.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=self.gnTextBox.yview)

                Button(self.gn, text = "Exit Window", command = lambda: self.gn.destroy()).pack(fill = X)

                def doGN(points, R, vk, k, _lambda, it):
                    i = 0
                    all_points = []
                    while i < len(points):
                        all_points.append(["", ""])
                        all_points[i][0] = points[i][0].get()
                        all_points[i][1] = points[i][1].get()
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

                    all_R = []
                    i = 0
                    while i < len(R):
                        all_R.append("")
                        all_R[i] = float(R[i].get())
                        i += 1

                    all_vk = [[""], [""]]
                    all_vk[0][0] = vk[0].getdouble()
                    all_vk[1][0] = vk[1].getdouble()

                    K = k.get()
                    if not K.isdigit():
                        K = "null"

                    iterations = int(it.get())
                    if _type == 1:
                        lmbda = float(_lambda.get())
                    else:
                        lmbda = 0

                    solutions = []
                    rmse = []

                    base_str_x = "(x xi) / sqrt((x xi)^2 + (y yi)^2)"
                    base_str_y = "(y yi) / sqrt((x xi)^2 + (y yi)^2)"
                    base_str_rk = "sqrt((x xi)^2 + (y yi)^2) Ri K"

                    _it = 0
                    start_time = timeit.default_timer()
                    while _it < iterations:
                        i = 0
                        A = []
                        while i < len(x):
                            if K == "null":
                                A.append(["", ""])
                            else:
                                A.append(["", "", ""])
                            A0_str = base_str_x.replace(" xi", "%+f" % (x[i] * -1))
                            A0_str = A0_str.replace(" yi", "%+f" % (y[i] * -1))
                            A[i][0] = f(all_vk[0][0], A0_str, all_vk[1][0])
                            A1_str = base_str_y.replace(" xi", "%+f" % (x[i] * -1))
                            A1_str = A1_str.replace(" yi", "%+f" % (y[i] * -1))
                            A[i][1] = f(all_vk[0][0], A1_str, all_vk[1][0])
                            if K != "null":
                                A[i][2] = -1
                            i += 1

                        i = 0
                        rk = []
                        while i < len(x):
                            rk.append([""])
                            r0_str = base_str_rk.replace(" xi", "%+f" % (x[i] * -1))
                            r0_str = r0_str.replace(" yi", "%+f" % (y[i] * -1))
                            r0_str = r0_str.replace("Ri", "%+f" % (all_R[i] * -1))
                            set_k = 0
                            if K != "null":
                                set_k = float(K)
                            r0_str = r0_str.replace("K", "%+f" % (set_k * -1))
                            rk[i][0] = f(all_vk[0][0], r0_str, all_vk[1][0])
                            i += 1

                        ata = np.matmul(map(list, zip(*A)), A)
                        lhs = ata + (lmbda * np.diag(ata))
                        rhs = -1 * np.matmul(map(list, zip(*A)), rk)
                        all_vk = np.linalg.solve(lhs, rhs)
                        all_vk = all_vk.tolist()
                        solutions.append(all_vk)

                        inner_square = 0
                        for r in rk:
                            inner_square += float(r[0]) ** 2
                        rmse.append(math.sqrt(inner_square / float(len(rk))))
                        _it += 1

                    graph_x = []
                    i = 0
                    while i < iterations:
                        graph_x.append(i + 1)
                        i += 1
                    end_time = timeit.default_timer() - start_time

                    i = 0
                    for row in solutions:
                        _str = "Iteration " + str(i + 1) + ": " + str(row)
                        self.gnTextBox.insert(END, _str + '\n')
                    self.gnTextBox.insert(END, '\n')
                    i = 0
                    for row in rmse:
                        _str = "RMSE for Iteration " + str(i + 1) + ": " + str(row)
                        self.gnTextBox.insert(END, _str + '\n')
                    self.gnTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

                    plt.plot(graph_x, rmse)
                    plt.xlabel("Iterations")
                    plt.ylabel("RMSE")
                    plt.title("RMSE over Iterations")
                    plt.show()

    def diffMethodsWindow(self):
        # create Difference Methods window
        diffMethods = Toplevel()
        diffMethods.title("Difference Methods")
        diffMethods.resizable(0,0)
        mainFrame = Frame(diffMethods)
        mainFrame.pack(fill = "both")

        # f(x) label and entry box
        fLabel = Label(mainFrame, text = "f(x) = ").grid(row = 0, sticky = W)
        fEnt = Entry(mainFrame, width = 50)
        fEnt.grid(row = 0, sticky = W, padx = 30)

        # x Label
        xLabel = Label(mainFrame, text="x = ").grid(row=1, sticky=W)
        xEnt = Entry(mainFrame, width=10)
        xEnt.grid(row=1, sticky=W, padx=30)

        # h Label
        hLabel = Label(mainFrame, text="h = ").grid(row=2, sticky=W)
        hEnt = Entry(mainFrame, width=10)
        hEnt.grid(row=2, sticky=W, padx=30)

        # Submit Button
        submitBtn = Button(mainFrame, text = "Submit", command=lambda: doDiffMethods(fEnt.get(), xEnt.get(), hEnt.get()))
        submitBtn.grid(row=3, pady = 10)

        resultFrame = Frame(diffMethods)
        resultFrame.pack(fill="x")

        scrollbar = Scrollbar(resultFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        diffTextBox = Text(resultFrame)
        diffTextBox.pack(fill="both")
        diffTextBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=diffTextBox.yview)

        Button(diffMethods, text = "Exit Window", command = lambda: diffMethods.destroy()).pack(fill = X)

        def doDiffMethods(fstr, x, h):
            def analytic(_fstr, x):
                _fstr = format(1, _fstr, ['x'])
                _fstr = parse_expr(_fstr)
                _fstr = str(diff(_fstr))
                result = f(x, _fstr)
                return result

            def forward(_fstr, x, h):
                term1 = float(f(x + h, _fstr))
                term2 = float(f(x, _fstr))
                result = (term1 - term2) / h
                return result

            def backward(_fstr, x, h):
                term1 = float(f(x, _fstr))
                term2 = float(f(x - h, _fstr))
                result = (term1 - term2) / h
                return result

            def centered(_fstr, x, h):
                term1 = float(f(x + h, _fstr))
                term2 = float(f(x - h, _fstr))
                result = (term1 - term2) / (2 * h)
                return result

            def get_error(_fstr, result, x):
                real_deriv = analytic(_fstr, x)
                result = abs(result - real_deriv)
                return result

            _fstr = str(fstr)
            x = float(x)
            h = float(h)
            start_time = timeit.default_timer()
            f_error = forward(_fstr, x, h)
            b_error = backward(_fstr, x, h)
            c_error = centered(_fstr, x, h)
            diffTextBox.insert(END, "Two-Point Forward Difference: " + str(f_error) + '\n')
            diffTextBox.insert(END, "Two-Point Backward Backward Difference: " + str(b_error) + '\n')
            diffTextBox.insert(END, "Three-Point Centered Difference: " + str(c_error) + '\n\n')
            diffTextBox.insert(END, "Forward Difference Error: " + str(get_error("1/x", f_error, x)) + '\n')
            diffTextBox.insert(END, "Backward Difference Error: " + str(get_error("1/x", b_error, x)) + '\n')
            diffTextBox.insert(END, "Centered Difference Error: " + str(get_error("1/x", c_error, x)) + '\n\n')
            end_time = timeit.default_timer() - start_time
            self.text_box.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def extrapWindow(self):
        # create Extrapolation window
        extrap = Toplevel()
        extrap.title("Extrapolation")
        extrap.resizable(0,0)
        mainFrame = Frame(extrap)
        mainFrame.pack(fill = "both")

        # f(x) label and entry box
        fLabel = Label(mainFrame, text="f(x) = ").grid(row=0, sticky=W)
        fEnt = Entry(mainFrame, width=50)
        fEnt.grid(row=0, column=1, sticky=W, padx=30)

        # x Label
        xLabel = Label(mainFrame, text="x = ").grid(row=1, sticky=W)
        xEnt = Entry(mainFrame, width=10)
        xEnt.grid(row=1, column=1, sticky=W, padx=30)

        # h Label
        hLabel = Label(mainFrame, text="h = ").grid(row=2, sticky=W)
        hEnt = Entry(mainFrame, width=10)
        hEnt.grid(row=2, column=1, sticky=W, padx=30)

        # order (n) Label
        nLabel = Label(mainFrame, text="Order (n) = ").grid(row=3, sticky=W)
        nEnt = Entry(mainFrame, width=10)
        nEnt.grid(row=3, column=1, sticky=W, padx=30)

        # Submit Button
        submitBtn = Button(mainFrame, text="Submit", command=lambda: doExtra(fEnt.get(), xEnt.get(), hEnt.get(), nEnt.get()))
        submitBtn.grid(row=4, pady=10)

        resultFrame = Frame(extrap)
        resultFrame.pack(fill="x")

        scrollbar = Scrollbar(resultFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        extraTextBox = Text(resultFrame)
        extraTextBox.pack(fill="both")
        extraTextBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=extraTextBox.yview)

        Button(extrap, text="Exit Window", command=lambda: extrap.destroy()).pack(fill=X)

        def doExtra(fstr, x, h, n):
            def richardson(_fstr, x, n, h):
                d = np.array([[0] * (n + 1)] * (n + 1), float)
                for i in xrange(n + 1):
                    d[i, 0] = 0.5 * (f(x + h, _fstr) - f(x - h, _fstr)) / h
                    powerOf4 = 1
                    for j in xrange(1, i + 1):
                        powerOf4 = 4 * powerOf4
                        d[i, j] = d[i, j - 1] + (d[i, j - 1] - d[i - 1, j - 1]) / (powerOf4 - 1)
                    h = 0.5 * h
                return d[n, n]

            n = int(n)
            x = float(x)
            h = float(h)
            _fstr = str(fstr)
            start_time = timeit.default_timer()
            Q = richardson(_fstr, x, n, h)
            end_time = timeit.default_timer() - start_time
            extraTextBox.insert(END, "Richardson Extrapolation yields Q = " + str(Q) + '\n')
            extraTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def adWindow(self):
        # create Automatic Differentiation window
        ad = Toplevel()
        ad.title("Automatic Differentiation")
        ad.resizable(0,0)
        mainFrame = Frame(ad)
        mainFrame.pack(fill = "both")

        # f(x) Label
        Label(mainFrame, text = "Enter f(g)").grid(row = 0, sticky = W)

        # f(g) label and entry box
        Label(mainFrame, text = "f(g), ex: ln(g), e^g, tan(g) + 2*x").grid(row = 1, sticky = W, padx = 30)
        fLabel = Label(mainFrame, text = "f(g):").grid(row = 2, sticky = W)
        fEnt = Entry(mainFrame, width = 50)
        fEnt.grid(row = 2, sticky = W, padx = 30)

        # g(x) label and entry box
        Label(mainFrame, text = "g(x), ex: 2*x*x*x + 4*x + 5").grid(row = 3, sticky = W, padx = 30)
        gLabel = Label(mainFrame, text = "g(x):").grid(row = 4, sticky = W)
        gEnt = Entry(mainFrame, width = 50)
        gEnt.grid(row = 4, sticky = W, padx = 30)

        # x label and entry box
        xLabel = Label(mainFrame, text="x = ").grid(row=5, sticky=W)
        xEnt = Entry(mainFrame, width=50)
        xEnt.grid(row=5, sticky=W, padx = 30)

        # Submit Button
        submitBtn = Button(mainFrame, text = "Submit", command=lambda: doAD(fEnt.get(), gEnt.get(), xEnt.get()))
        submitBtn.grid(row = 6, pady = 10)

        resultFrame = Frame(ad)
        resultFrame.pack(fill="x")

        scrollbar = Scrollbar(resultFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        adTextBox = Text(resultFrame)
        adTextBox.pack(fill="both")
        adTextBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=adTextBox.yview)

        Button(ad, text = "Exit Window", command = lambda: ad.destroy()).pack(fill = X)

        def doAD(f, g, x):
            x = float(x)
            start_time = timeit.default_timer()
            g = format(0, g, ['x'])
            autoDiff = forwardAutoDiff(format(0, f, ['g']), g, x)
            gValues = float(autoDiff.calcG()), float(autoDiff.g_deriv())
            result = (autoDiff.calcF(), autoDiff.f_deriv())
            end_time = timeit.default_timer() - start_time

            adTextBox.insert(END, '\nx = ' + str(x) + '\n')
            adTextBox.insert(END, 'g(x) = ' + str(autoDiff.g) + '\n')
            adTextBox.insert(END, 'g(x), g\'(x) at x = ' + str(float(autoDiff.x)) + ': ' + str(gValues) + '\n')
            adTextBox.insert(END, 'f = ' + str(autoDiff.f) + '\n')
            adTextBox.insert(END, 'S(f, f\') = ' + str(result) + '\n\n')
            adTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def nCodesWindow(self):
        # create Newton Codes window
        nCodes = Toplevel()
        nCodes.title("Newton-Cotes")
        nCodes.resizable(0,0)
        mainFrame = Frame(nCodes)
        mainFrame.pack(fill = "both")

        # f label and entry box
        fLabel = Label(mainFrame, text = "f(x):").grid(row = 0, sticky = W)
        fEnt = Entry(mainFrame, width = 40)
        fEnt.grid(row = 0, sticky = W, padx = 50)

        # limits of integration

        # a label and entry box
        Label(mainFrame, text = "Limits of integration:").grid(row = 1, sticky = W)
        aLabel = Label(mainFrame, text = "a:").grid(row = 2, sticky = W)
        a = Entry(mainFrame, width = 40)
        a.grid(row = 2, sticky = W, padx = 50)
        # b label and entry box
        bLabel = Label(mainFrame, text = "b:").grid(row = 3, sticky = W)
        b = Entry(mainFrame, width = 40)
        b.grid(row = 3, sticky = W, padx = 50)

        # number of intervals label and entry box
        nLabel = Label(mainFrame, text = "# of intervals:").grid(row = 4, sticky = W)
        n = Entry(mainFrame, width = 35)
        n.grid(row = 4, sticky = W, padx = 80)

        # Submit Button
        submitBtn = Button(mainFrame, text = "Submit", command = lambda: doNCodes(fEnt.get(), int(a.get()), int(b.get()), int(n.get())))
        submitBtn.grid(row = 6, pady = 10)

        resultFrame = Frame(nCodes)
        resultFrame.pack(fill="x")

        scrollbar = Scrollbar(resultFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        nCodesTextBox = Text(resultFrame)
        nCodesTextBox.pack(fill="both")
        nCodesTextBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=nCodesTextBox.yview)

        Button(nCodes, text = "Exit Window", command = lambda: nCodes.destroy()).pack(fill = X)

        def doNCodes(func, a, b, n):
            fstr = str(func)
            a = float(a)
            b = float(b)
            n = int(n)

            def roundoff_error(fstr, a, b):
                e_mach = np.finfo(float).eps
                _fstr = format(1, fstr, ['x'])
                _fstr = parse_expr(_fstr)
                _fstr = str(diff(diff(diff(_fstr))))
                c = (b + a) / 2
                h = b - a
                result = (((h**2) / float(6)) * (f(c, _fstr))) + (e_mach / float(h))
                return result

            # call integration routines
            t_start_time = timeit.default_timer()
            trap = trapezoid(fstr, a, b, n)
            terr = trap_error(fstr, a, b)
            t_end_time = timeit.default_timer() - t_start_time
            s_start_time = timeit.default_timer()
            simp = simpson(fstr, a, b, n)
            serr = simp_error(fstr, a, b)
            s_end_time = timeit.default_timer() - s_start_time

            # print results
            nCodesTextBox.insert(END, '\nMethod            Solution    Numerical Error      Execution Time\n' )
            nCodesTextBox.insert(END, '-------------------------------------------------------------------\n' )
            nCodesTextBox.insert(END, 'Trapezoid      %12.6f   %6.3f               %f seconds\n'  % (trap, terr, t_end_time),'%' + '\n' )
            nCodesTextBox.insert(END, 'Simpson        %12.6f   %6.3f               %f seconds\n'  % (simp, serr, s_end_time),'%' + '\n\n' )
            nCodesTextBox.insert(END, "\nRoundoff Error E(h) = " + str(roundoff_error(fstr, a, b)) + " (upper bound)")

    def rombergWindow(self):
        # create romberg window
        romb = Toplevel()
        romb.title("Romberg")
        romb.resizable(0,0)
        mainFrame = Frame(romb)
        mainFrame.pack(fill = "both")

        # f label and entry box
        fLabel = Label(mainFrame, text = "f(x):").grid(row = 0, sticky = W)
        fEnt = Entry(mainFrame, width = 40)
        fEnt.grid(row = 0, sticky = W, padx = 50)

        #limits of integration

        # a label and entry box
        Label(mainFrame, text = "Limits of integration:").grid(row = 1, sticky = W)
        aLabel = Label(mainFrame, text = "a:").grid(row = 2, sticky = W)
        a = Entry(mainFrame, width = 40)
        a.grid(row = 2, sticky = W, padx = 50)
        # b label and entry box
        bLabel = Label(mainFrame, text = "b:").grid(row = 3, sticky = W)
        b = Entry(mainFrame, width = 40)
        b.grid(row = 3, sticky = W, padx = 50)

        # number of intervals label and entry box
        nLabel = Label(mainFrame, text = "# of intervals:").grid(row = 4, sticky = W)
        n = Entry(mainFrame, width = 35)
        n.grid(row = 4, sticky = W, padx = 80)

        # Submit Button
        submitBtn = Button(mainFrame, text = "Submit", command = lambda: doRomberg(fEnt.get(), int(a.get()), int(b.get()), int(n.get())))
        submitBtn.grid(row = 6, pady = 10)

        resultFrame = Frame(romb)
        resultFrame.pack(fill="x")

        scrollbar = Scrollbar(resultFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        romTextBox = Text(resultFrame)
        romTextBox.pack(fill="both")
        romTextBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=romTextBox.yview)

        Button(romb, text = "Exit Window", command = lambda: romb.destroy()).pack(fill="both")

        def doRomberg(func, a, b, n):
            fstr = str(func)
            a = float(a)
            b = float(b)
            start_time = timeit.default_timer()
            romb = romberg(fstr, a, b, n)
            end_time = timeit.default_timer() - start_time
            romTextBox.insert(END, 'Romberg: ' + str(romb) + '\n')
            self.text_box.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def quadraWindow(self):
        # create Adaptive window
        quad = Toplevel()
        quad.title("Quadrature")
        quad.resizable(0,0)

        Button(quad, text = "Adaptive", width = 40, command = lambda: adaptiveWindow()).pack(fill = "both")
        Button(quad, text = "Gaussian", command = lambda: gaussianWindow()).pack(fill = "both")
        Button(quad, text = "Exit Window", command = lambda: quad.destroy()).pack(fill="both")

        def adaptiveWindow():
            adapt = Toplevel()
            adapt.title("Adaptive Quadrature")
            adapt.resizable(0,0)
            mainFrame = Frame(adapt)
            mainFrame.pack(fill = "both")

            # f label and entry box
            fLabel = Label(mainFrame, text = "f(x):").grid(row = 0, sticky = W)
            fEnt = Entry(mainFrame, width = 40)
            fEnt.grid(row = 0, sticky = W, padx = 50)

            #limits of integration

            # a label and entry box
            Label(mainFrame, text = "Limits of integration:").grid(row = 1, sticky = W)
            aLabel = Label(mainFrame, text = "a:").grid(row = 2, sticky = W)
            a = Entry(mainFrame, width = 40)
            a.grid(row = 2, sticky = W, padx = 50)
            # b label and entry box
            bLabel = Label(mainFrame, text = "b:").grid(row = 3, sticky = W)
            b = Entry(mainFrame, width = 40)
            b.grid(row = 3, sticky = W, padx = 50)

            # Submit Button
            submitBtn = Button(mainFrame, text = "Submit", command = lambda: doAdaptive(fEnt.get(), a.get(), b.get()))
            submitBtn.grid(row = 6, pady = 10)

            resultFrame = Frame(adapt)
            resultFrame.pack(fill="x")

            scrollbar = Scrollbar(resultFrame)
            scrollbar.pack(side=RIGHT, fill=Y)

            adaptTextBox = Text(resultFrame)
            adaptTextBox.pack(fill="both")
            adaptTextBox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=adaptTextBox.yview)

            Button(adapt, text = "Exit Window", command = lambda: adapt.destroy()).pack(fill="both")

            def doAdaptive(f, a, b):
                fstr = str(f)
                a = float(a)
                b = float(b)
                start_time = timeit.default_timer()
                x = Symbol('x')
                fstr = lambdify(x, parse_expr(format(1, fstr, ['x'])))
                result = scipy.integrate.quad(fstr, a, b)[0]
                end_time = timeit.default_timer() - start_time
                adaptTextBox.insert(END, "Adaptive Quadrature yields: " + str(result) + "\n")
                adaptTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

        def gaussianWindow():
            gauss = Toplevel()
            gauss.title("Gaussian Quadrature")
            gauss.resizable(0,0)
            mainFrame = Frame(gauss)
            mainFrame.pack(fill = "both")

            # f label and entry box
            fLabel = Label(mainFrame, text = "f(x):").grid(row = 0, sticky = W)
            fEnt = Entry(mainFrame, width = 40)
            fEnt.grid(row = 0, sticky = W, padx = 50)

            #limits of integration

            # a label and entry box
            Label(mainFrame, text = "Limits of integration:").grid(row = 1, sticky = W)
            aLabel = Label(mainFrame, text = "a:").grid(row = 2, sticky = W)
            a = Entry(mainFrame, width = 40)
            a.grid(row = 2, sticky = W, padx = 50)
            # b label and entry box
            bLabel = Label(mainFrame, text = "b:").grid(row = 3, sticky = W)
            b = Entry(mainFrame, width = 40)
            b.grid(row = 3, sticky = W, padx = 50)

            # Submit Button
            submitBtn = Button(mainFrame, text = "Submit", command = lambda: doGauss(fEnt.get(), a.get(), b.get()))
            submitBtn.grid(row = 6, pady = 10)

            resultFrame = Frame(gauss)
            resultFrame.pack(fill="x")

            scrollbar = Scrollbar(resultFrame)
            scrollbar.pack(side=RIGHT, fill=Y)

            gaussTextBox = Text(resultFrame)
            gaussTextBox.pack(fill="both")
            gaussTextBox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=gaussTextBox.yview)

            Button(gauss, text = "Exit Window", command = lambda: gauss.destroy()).pack(fill="both")

            def doGauss(f, a, b):
                fstr = str(f)
                a = float(a)
                b = float(b)
                start_time = timeit.default_timer()
                x = Symbol('x')
                fstr = lambdify(x, parse_expr(format(1, fstr, ['x'])))
                result = quadrature(np.vectorize(fstr), a, b)[0]
                end_time = timeit.default_timer() - start_time
                gaussTextBox.insert(END, "Gaussian Quadrature yields: " + str(result) + "\n")
                gaussTextBox.insert(END, "Execution Time = " + str(end_time) + " seconds\n")

    def start(self):
        self.root.mainloop()

    def quitApp(self):
        self.root.destroy()

# create the application
gui = App()

# start the program
gui.start()
