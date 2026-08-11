import sympy as sp 
from sympy.utilities.lambdify import lambdify
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # figurecanvas -> allows matplot graph to be inside Qt window
from matplotlib.figure import Figure # figure -> the graph itself

x = sp.symbols('x') # x = mathematical variable 

def graph_x_squared(): # WILL GO AWAY EVEENTUALLY
    x = np.linspace(-10,10,100) # create 100 evenly spaced numbers starting -10 to 10 & store in x
    y = x**2

    
    axis.plot(x,y) # adding axis bc figure sint in seperate window anymore 

    axis.set_xlabel("x") # name the axis
    axis.set_ylabel("y")
    axis.set_title("math visualizer") # name the graph
    axis.grid()

    canvas.draw() # draw the canvas to update the graph


app = QApplication([])

figure = Figure()
axis = figure.add_subplot(111) 
canvas = FigureCanvas(figure) 

#print("Choose a function: ")
#print ("1. x^2")
#print ("2. x^3")
#print ("3. 2x + 1")
#print ("4. sin(x)")

# choice = input ("Choose a function (1-4): ")

#def f(x):
    #if choice == "1": # in "" because input gives string
        #return x**2
    #elif choice == "2":
        #return x**3
    #elif choice == "3":
        #return 2*x+1
    #elif choice == "4":
        #return np.sin(x)
    #else:
        #print("Invalid choice.")

#x = np.linspace(-10,10,100) # create 100 evenly spaced numbers starting -10 to 10 & store in x
#y = f(x)

#plt.plot(x,y) # take x and y and draw a line connecting them 
#plt.xlabel("x") # name the axis
#plt.ylabel("y")
#plt.title("math visualizer") # name the graph
#plt.grid()
#plt.show() # display the plot

def update_graph():
    equation = equation_input.text()
    expression = sp.sympify(equation)  # Convert the input string to a sympy expression
    x_values = np.linspace(-10, 10, 400)
    function = lambdify (x, expression, "numpy")  # Convert the sympy expression to a numpy function
    y_values = function(x_values)

    axis.clear()
    axis.plot(x_values, y_values)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_title("Graph Visualizer")
    axis.grid()
    canvas.draw()

#def plot_graph(y, title):
    #x = np.linspace(-10, 10, 400)
    #axis.clear()  # Clear the previous plot
    #axis.plot(x, y)
    #axis.set_title(title)
    #canvas.draw()


window = QWidget()
window.setWindowTitle("Math Visualizer")
window.resize(800, 600)
layout = QVBoxLayout(window) # QVboxLayout -> layout manager that arranges widgets vertically
controls = QWidget() # create a widget to hold the controls
controls_layout = QVBoxLayout(controls) # create a layout for the controls

equation_input = QLineEdit()
equation_input.setPlaceholderText("Enter an equation...")
controls_layout.addWidget(equation_input)

equation_input.returnPressed.connect(update_graph) # when user presses enter, update graph

button = QPushButton("Graph x^2") #adding a button 
#layout.addWidget(button) # add button to layout

#figure = Figure() # figure -> matplot graph container (where graph will be)
#canvas = FigureCanvas(figure) # figurecanvas -> allows matplot graph to be inside Qt


top_layout = QHBoxLayout() # top section -> graph + controls
top_layout.addWidget(canvas,2) # graph on left
top_layout.addWidget(controls,3) # controls on right
layout.addLayout(top_layout) # add top section to main layout
layout.addWidget(button) # add button underneath 

button.clicked.connect(graph_x_squared) #clicks button -> button.clicked -> graph_x_squared -> python does smth

window.show()
app.exec()