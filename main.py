import sympy as sp 
from sympy.utilities.lambdify import lambdify
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # figurecanvas -> allows matplot graph to be inside Qt window
from matplotlib.figure import Figure # figure -> the graph itself

x = sp.symbols('x') # x = mathematical variable 


app = QApplication([])

figure = Figure()
axis = figure.add_subplot(111) 
canvas = FigureCanvas(figure) 


def update_graph():
    equation = equation_input.get_equation()
    # sqrt translator
    equation = equation.replace("√", "sqrt")  # Replace the square root symbol with sympy's sqrt function
    # pi translator
    equation = equation.replace("π", "pi")  # Replace the pi symbol with sympy's pi function
    # infinity translator
    equation = equation.replace("∞", "oo")  # Replace the infinity symbol with sympy's oo (infinity) function

    print ("Equation sent to SymPy: ", equation)

    try:
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

    except Exception as e:
        print ("Error: ", e)

#def plot_graph(y, title):
    #x = np.linspace(-10, 10, 400)
    #axis.clear()  # Clear the previous plot
    #axis.plot(x, y)
    #axis.set_title(title)
    #canvas.draw()

class ExponentBox (QLineEdit):
    def __init__ (self, editor, position):
        super().__init__()

        self.editor = editor
        self.position = position

        self.setFixedSize(35,22)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.clearFocus()
            self.editor.text.setFocus()
            self.editor.text.setCursorPosition(self.position)

        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
            self.editor.text.setFocus()
            update_graph()

        else:
            super().keyPressEvent(event)

class EquationEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.text = QLineEdit()
        self.text.setPlaceholderText("Enter an equation...")

        self.text.setParent(self)
        self.text.returnPressed.connect(update_graph)

        self.exponents = []
        self.setMinimumHeight(50)

    def resizeEvent(self, event):
        self.text.setGeometry(0,5, self.width(), 40)   
        super().resizeEvent(event)

    def add_exponent (self):
        position = self.text.cursorPosition()

        exponent_box = ExponentBox(self, position)
        self.exponents.append(exponent_box)
        exponent_box.show()

        cursor_rect = self.text.cursorRect()

        exponent_box.move(cursor_rect.x(),0) # cursor_rect.y() - 15)

        exponent_box.show()
        exponent_box.raise_()
        exponent_box.setFocus()


    def get_equation (self):
        equation = self.text.text()

        for exponent_box in reversed(self.exponents): 
            exponent = exponent_box.text()

            if exponent:
                position = exponent_box.position
                exponent = exponent.replace("√", "sqrt")
                exponent = exponent.replace("π", "pi")
                exponent = exponent.replace("∞", "oo")

                equation=(equation[:position]+ "**(" + exponent + ")" + equation[position:])
        
        return equation 


    def insert (self,text):
        self.text.insert(text)   

def clear_equation():
    equation_input.text.clear()

    for exponent_box in equation_input.exponents:
        exponent_box.deleteLater()

    equation_input.exponents.clear()
    equation_input.text.setFocus()
    
window = QWidget()
window.setWindowTitle("Math Visualizer")
window.resize(800, 600)
layout = QVBoxLayout(window) # QVboxLayout -> layout manager that arranges widgets vertically
controls = QWidget() # create a widget to hold the controls
controls_layout = QVBoxLayout(controls) # create a layout for the controls

equation_input = EquationEditor() 
controls_layout.addWidget(equation_input)

# clear button
clear_button = QPushButton ("Clear")
controls_layout.addWidget(clear_button)
clear_button.clicked.connect(clear_equation)

# sqrt button
sqrt_button = QPushButton("√")
controls_layout.addWidget(sqrt_button)
sqrt_button.clicked.connect(lambda: equation_input.insert("√(")) # when click button -> program sees "sqrt("

# pi button
pi_button = QPushButton("π")
controls_layout.addWidget(pi_button)
pi_button.clicked.connect(lambda: equation_input.insert("π")) 

# exponenet button
exponent_button = QPushButton("x²")
controls_layout.addWidget(exponent_button)
exponent_button.clicked.connect(equation_input.add_exponent) 

# infinity button
infinity_button = QPushButton("∞")
controls_layout.addWidget(infinity_button)
infinity_button.clicked.connect(lambda: equation_input.insert("∞")) 

#equation_input.returnPressed.connect(update_graph) # when user presses enter, update graph

#layout.addWidget(button) # add button to layout

#figure = Figure() # figure -> matplot graph container (where graph will be)
#canvas = FigureCanvas(figure) # figurecanvas -> allows matplot graph to be inside Qt


top_layout = QHBoxLayout() # top section -> graph + controls
top_layout.addWidget(canvas,2) # graph on left
top_layout.addWidget(controls,3) # controls on right
layout.addLayout(top_layout) # add top section to main layout

window.show()
app.exec()