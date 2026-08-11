import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # figurecanvas -> allows matplot graph to be inside Qt window
from matplotlib.figure import Figure # figure -> the graph itself

def graph_x_squared():
    x = np.linspace(-10,10,100) # create 100 evenly spaced numbers starting -10 to 10 & store in x
    y = x**2

    axis = figure.add_subplot(111) # add a subplot to the figure (1 row, 1 column, 1st plot)
    axis.plot(x,y) # adding axis bc figure sint in seperate window anymore 

    axis.set_xlabel("x") # name the axis
    axis.set_ylabel("y")
    axis.set_title("math visualizer") # name the graph
    axis.grid()

    canvas.draw() # draw the canvas to update the graph


app = QApplication([])

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

window = QWidget()
window.setWindowTitle("Math Visualizer")
window.resize(800, 600)
layout = QVBoxLayout(window) # QVboxLayout -> layout manager that arranges widgets vertically

button = QPushButton("Graph x^2") #adding a button 
layout.addWidget(button) # add button to layout

figure = Figure() # figure -> matplot graph container (where graph will be)
canvas = FigureCanvas(figure) # figurecanvas -> allows matplot graph to be inside Qt
layout.addWidget(canvas) 

button.clicked.connect(graph_x_squared) #clicks button -> button.clicked -> graph_x_squared -> python does smth

window.show()
app.exec()