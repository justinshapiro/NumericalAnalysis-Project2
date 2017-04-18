# Numerical Analysis - Project2

Code for Team 2.3 - Project 2

DUE April 28th (tentative)

To be done in Python 2.7.13 and deployed for Team 1.3

Windows version will be compiled to .exe using py2exe, Mac runs Python 2.7 natively. The goal is users should not need to install Python to run this, although Mac users may have to `pip` some libraries.


**Roles**

 1. Patricia Figueroa - Method research & implementation
 2. Justin Shapiro - Implementation, deployment and user support
 3. Jonathan Pham - GUI development & wholesome integration of parts
 4. Rachel Wiggins - User reference manual, assist with testing
 5. Omer Sarwana - Software testing, assist with GUI

**Software must implement all of the bullet pointed methods:**

A. Interpolation

 - Chebyshev -- DONE
 - Splines (cubic) -- DONE
 - Bezier -- DONE

B. Least Squares

 - Linear
    - Classical Gram-Schmidt
    - Modified Gram-Schmidt
    - Householder Reflectors
    - QR Factorization -- DONE
 - Nonlinear
    - Gauss-Newton
    - Levenberg-Marquardt

C. Differentiation and Integration

 - Differentiation
	 - Difference Methods
	 - Extrapolation
	 - Automatic Differentiation (professor's notes/references)
 - Integration
	 - Newton-Codes - Trapezoidal, Simpson
	 - Romberg
	 - Adaptive
		 - Gaussian
