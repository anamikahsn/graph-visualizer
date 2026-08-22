import sympy as sp 
from sympy.utilities.lambdify import lambdify
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QSlider, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # figurecanvas -> allows matplot graph to be inside Qt window
from matplotlib.figure import Figure # figure -> the graph itself

x, a = sp.symbols('x a') # x = mathematical variable 
active_equation = None
app = QApplication([])

figure = Figure(facecolor = "#EBEBE9")
axis = figure.add_subplot(111) 
axis.set_facecolor("#EBEBE9")
canvas = FigureCanvas(figure) 

def update_all_graphs():
    axis.clear()

    for equation_input in equation_editors:
        equation = equation_input.get_equation()

        # sqrt translator
        equation = equation.replace("√", "sqrt")  # Replace the square root symbol with sympy's sqrt function
        # pi translator
        equation = equation.replace("π", "pi")  # Replace the pi symbol with sympy's pi function
        # infinity translator
        #equation = equation.replace("∞", "oo")  # Replace the infinity symbol with sympy's oo (infinity) function
        # ln translator
        equation = equation.replace("ln(", "log(")

        if not equation.strip():
            continue

        print("Equation sent to Sympty", equation)

        try:
            local_dict = {
                "ln": sp.log,
                "log10": lambda value: sp.log(value, 10),
                "sqrt": sp.sqrt,
                "pi": sp.pi,
                #"oo": sp.oo
            }

            expression = sp.sympify (equation, locals = local_dict)

            x_values = np.linspace(-10,10,400)

            slider_values = {}

            for variable in expression.free_symbols:
                if variable != x:

                    if variable in equation_input.sliders:
                        slider_values[variable] = equation_input.sliders[variable].value()
                    else:
                        slider_values[variable] = 1

            function = lambdify([x, *slider_values.keys()], expression, "numpy")
            y_values = function(x_values, *slider_values.values())
            axis.plot(x_values, y_values, color="#4A533C")

        except Exception as e:
            print ("Error:", e)

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

class ExponentBox (QLineEdit):
    def __init__ (self, editor, position): 
        super().__init__(editor)

        self.editor = editor
        self.position = position

        self.setFixedSize(30,18)

        small_font = QFont()
        small_font.setPointSize(9)
        self.setFont(small_font)

        self.selectAll()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.clearFocus()
            self.editor.text.setFocus()
            self.editor.text.setCursorPosition(self.position)

        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
            self.editor.text.setFocus()
            update_all_graphs()

        else:
            super().keyPressEvent(event)

class NRootBox (QLineEdit):
    def __init__(self, editor, position):
        super().__init__(editor)

        self.editor = editor 
        self.position = position

        self.setFixedSize(25,18)

        small_font = QFont()
        small_font.setPointSize(9)
        self.setFont(small_font)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.clearFocus()
            self.editor.text.setFocus()
            self.editor.text.setCursorPosition(self.position)

        elif event.key() ==Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
            self.editor.text.setFocus()
            update_all_graphs()

        else:
            super().keyPressEvent(event)

class AbsoluteValueBox (QLineEdit):
    def __init__(self, editor, position):
        super().__init__(editor)

        self.editor = editor
        self.position = position

        self.setFixedSize(30,22)

        small_font = QFont()
        small_font.setPointSize(10)
        self.setFont(small_font)

        self.setAlignment (Qt.AlignCenter)
        self.setStyleSheet ("""
            QLineEdit {
                border: none;
                border-left: 2px solid black;
                border-right: 2px solid black;
                background: transparent;
                padding: 0 4px;
            }
        """)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Right:        # right arrow -> main equation
            self.clearFocus()
            self.editor.text.setFocus()
            self.editor.text.setCursorPosition(self.position)

        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
            self.editor.text.setFocus()
            update_all_graphs()

        else:
            super().keyPressEvent(event)

equation_editors = []

class EquationLineEdit (QLineEdit):
    def __init__(self, editor):
        self.editor = editor

    def focusInEvent(self, event):
        global active_equation

        active_equation = self.editor
        super().focusInEvent(event)

class EquationEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.text = QLineEdit()
        self.text.setFocusPolicy(Qt.StrongFocus)
        self.text.setPlaceholderText("Enter an equation...")

        self.text.setStyleSheet("""
            QLineEdit {
                background-color: #B5C99A;
                border: 2px solid #7E8C6B;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.text.setParent(self)
        self.text.returnPressed.connect(update_all_graphs)      
        self.text.returnPressed.connect(update_sliders)

        self.exponents = []
        self.absolute_values = []
        self.n_roots = []
        self.setMinimumHeight(50)

    def resizeEvent(self, event):
        self.text.setGeometry(0,5, self.width(), 40)   
        super().resizeEvent(event)

    def add_exponent (self):
        position = self.text.cursorPosition()

        exponent_box = ExponentBox(self, position)
        self.exponents.append(exponent_box)
        #exponent_box.show()

        cursor_rect = self.text.cursorRect()

        exponent_box.move(self.text.x() + cursor_rect.x(), self.text.y() - 12)

        exponent_box.show()
        exponent_box.raise_()
        exponent_box.setFocus()

    def add_n_root(self):
        position = self.text.cursorPosition()

        self.insert("√")
        root_box = NRootBox(self, position)

        self.n_roots.append(root_box)
        cursor_rect = self.text.cursorRect()

        root_box.move(self.text.x() + cursor_rect.x() - 5, self.text.y() - 12)

        root_box.show()
        root_box.raise_()
        root_box.setFocus()

    def add_a_power(self):
        self.insert("a")          # insert a first 
        self.add_exponent()       # exponent box right after

    def add_absolute_value(self):
        position = self.text.cursorPosition()
        absolute_box = AbsoluteValueBox(self, position)
        self.absolute_values.append(absolute_box)
        cursor_rect = self.text.cursorRect()

        # center vertically within text field instead of floating above it
        y = self.text.y() + (self.text.height() - absolute_box.height()) // 2
        absolute_box.move (self.text.x() + cursor_rect.x(), y)

        absolute_box.show()
        absolute_box.raise_()
        absolute_box.setFocus()

    def get_equation (self):
        equation = self.text.text()

        for exponent_box in sorted (self.exponents, key=lambda box: box.position, reverse=True): 
            exponent = exponent_box.text()

            if exponent:
                position = exponent_box.position
                exponent = exponent.replace("√", "sqrt")
                exponent = exponent.replace("π", "pi")
                #exponent = exponent.replace("∞", "oo")

                equation=(equation[:position]+ "**(" + exponent + ")" + equation[position:])

        for absolute_box in sorted(self.absolute_values, key=lambda box: box.position,reverse=True):
            value = absolute_box.text()

            if value:
                position = absolute_box.position
                value = value.replace("√", "sqrt")
                value = value.replace("π", "pi")
                value = value.replace("∞", "oo")

                equation = (equation[:position] + "Abs(" + value + ")" + equation [position:])

        for root_box in sorted (self.n_roots, key=lambda box: box.position, reverse=True):
            root = root_box.text()

            if root:
                position = root_box.position

                sqrt_position = position

                if sqrt_position < len(equation) - 1:
                    value = equation[sqrt_position + 1]

                    equation = (equation[:sqrt_position] + "(" + value + ")**(1/" + root + ")" + equation[sqrt_position + 2:])
        
        return equation 


    def insert (self,text):
        self.text.insert(text)   

def update_sliders():
    while slider_layout.count():    # remove old sliders
        item = slider_layout.takeAt(0)

        if item.widget():
            item.widget().deleteLater()

    equation_input.sliders = {}

    equation = equation_input.get_equation()

    equation = equation.replace("√", "sqrt") 
    equation = equation.replace("π", "pi")  
    #equation = equation.replace("∞", "oo")  
    equation = equation.replace("ln(", "log(")

    try:
        expression = sp.sympify(equation)

        variables = expression.free_symbols
        variables = [v for v in variables if v != x]

        print("Variables found:", variables)

        for variable in sorted(variables, key=str):

            label = QLabel(str(variable))
            label.setStyleSheet("""
                QLabel {
                    color: #718355;
                    font-size: 16px;
                    font-weight: bold;
                    }
            """)

            slider = QSlider (Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(1)

            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    background: #B5C99A;
                    height: 6px;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #718355;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border-radius: 8px;
                }
                QSlider::sub-page:horizontal {
                    background: #718355;
                    border-radius: 3px;
                }
                QSlider::Add-page:horizontal {
                    background: #CFE1B9;
                    border-radius: 3px;
                }
            """)

            equation_input.sliders[variable] = slider
            slider.valueChanged.connect(update_all_graphs)

            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)

    except Exception as e:
        print ("Could not create sliders:", e)    

# + & - button colours
buttons_style = ("""
    QPushButton {
        background-color: #97A97C;
        border: none;
        border-radius: 5px;
        font-size: 20px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #87986A;
    }
    QPushButton:pressed {
        background-color: #718355;
    }
""")

def clear_equation():
    for editor in equation_editors:
        editor.text.clear()

        for exponent_box in editor.exponents: exponents_box.deleteLater()

        editor.exponents.clear()

        for absolute_box in editor.absolute_values:
            absolute_box.deleteLater()

        editor.absolute_values.clear()

        for root_box in editor.n_roots:
            root_box.deleteLater()

        editor.n_roots.clear()

    axis.clear()
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_title("Graph Visualizer")
    axis.grid()
    axis.draw()

    equation_input.text.setFocus()
    update_sliders()

def remove_equation(editor, row):
    if len(equation_editors) <= 1:
        return

    for box in editor.exponents:
        box.deleteLater()

    for box in editor.abosolute_values:
        box.deleteLater()

    for box in editor.n_roots:
        box.deleteLater()

    if editor in equation_editors:
        equation_editors.remove(editor)

    while row.count():
        item = row.takeAt(0)

        if item.widget():
            item.widget().deleteLater()

    equation_layout.removeItem(row)
    editor.deleteLater()
    update_all_graphs

def add_equation():
    new_equation = EquationEditor()
    equation_editors.append(new_equation)

    equation_row = QHBoxLayout()
    equation_row.addWidget(new_equation)

    plus_button = QPushButton("+")
    plus_button.setFixedWidth(35)
    plus_button.setStyleSheet(buttons_style)

    minus_button = QPushButton("-")
    minus_button.setFixedWidth(35)
    minus_button.setStyleSheet(buttons_style)

    equation_row.addWidget(plus_button)
    equation_row.addWidget(minus_button)

    equation_layout.addLayout(equation_row)

    plus_button.clicked.connect(add_equation)
    minus_button.clicked.connect(lambda: remove_equation(new_equation, equation_row))

    new_equation.text.setFocus()
    
window = QWidget()
window.setWindowTitle("Math Visualizer")
window.resize(1000, 800)

# colours
window.setStyleSheet("""
    QWidget {
        background-color: #E9F5DB;
    }
""")

main_layout = QGridLayout(window) # main 2x2 layout
main_layout.addWidget(canvas,0,0) # top left

slider_panel = QWidget()            # top right
slider_layout = QVBoxLayout(slider_panel)

#slider = QSlider(Qt.Horizontal)
#slider.setMinimum(-10)
#slider.setMaximum(10)
#slider.setValue(0)

#slider_layout.addWidget(slider)
main_layout.addWidget(slider_panel,0,1)

#slider.setStyleSheet("""
    #QSlider::groove:horizontal {
        #background: #B5C99A;
        #height: 6px;
        #border-radius: 3px
    #}
    #Qslider::handle:horizontal {
        #background: #718355;
        #width: 16px;
        #height: 16px
        #margin: -5px 0;
        #border-radius: 8px;
    #}
    #QSlider::sub=page:horizontal {
        #background: #718355;
        #border-radius: 3px;
    #}
    #QSlider::add-page:horizontal {
        #background: #CFE1B(;
        #border-radius: 3px;;
#""")

# bottom left
equation_panel = QWidget()
equation_layout = QVBoxLayout(equation_panel)

equation_editors = []  # keep track of every equations

equation_input = EquationEditor()
equation_editors.append(equation_input)
active_equation = equation_input

first_row = QHBoxLayout()
first_row.addWidget(equation_input)

plus_button = QPushButton("+")
plus_button.setFixedWidth(35)
plus_button.setStyleSheet(buttons_style)

minus_button = QPushButton("-")
minus_button.setFixedWidth(35)
minus_button.setStyleSheet(buttons_style)

first_row.addWidget(plus_button)
first_row.addWidget(minus_button)

equation_layout.addLayout(first_row)

plus_button.clicked.connect(add_equation)
minus_button.clicked.connect(lambda: remove_equation(equation_input, first_row))

main_layout.addWidget(equation_panel,1,0)

# bottom right
notation_panel = QWidget()
notation_layout = QGridLayout(notation_panel)

notation_button_style = """
    QPushButton {
        background-color: #B5C99A;
        border: none;
        border-radius: 5px;
        padding: 8px;
        font-size: 16px;
    }
    QPushButton:hover {
        background-color: #97A97C;
    }
    QPushButton:pressed {
        background-color: #87986A;
    }
"""

# clear button
clear_button = QPushButton ("Clear")
notation_layout.addWidget(clear_button,0,0,1,3)
clear_button.clicked.connect(clear_equation)
clear_button.setStyleSheet(notation_button_style)

# sqrt button
sqrt_button = QPushButton("√")
notation_layout.addWidget(sqrt_button,1,0)
sqrt_button.clicked.connect(lambda: active_equation.insert("√(")) # when click button -> program sees "sqrt("
sqrt_button.setStyleSheet(notation_button_style)

# pi button
pi_button = QPushButton("π")
notation_layout.addWidget(pi_button,1,1)
pi_button.clicked.connect(lambda: active_equation.insert("π")) 
pi_button.setStyleSheet(notation_button_style)

# exponenet button
exponent_button = QPushButton("x²")
notation_layout.addWidget(exponent_button,1,2)
exponent_button.clicked.connect(lambda: active_equation.add_exponent) 
exponent_button.setStyleSheet(notation_button_style)

# infinity button
#infinity_button = QPushButton("∞")
#notation_layout.addWidget(infinity_button)
#infinity_button.clicked.connect(lambda: equation_input.insert("∞")) 
#infinity_button.setStyleSheet(notation_button_style)

# ln button
ln_button = QPushButton("ln")
notation_layout.addWidget(ln_button,2,0)
ln_button.clicked.connect(lambda: active_equation.insert("ln("))
ln_button.setStyleSheet(notation_button_style)

# log button
log_button = QPushButton("log")
notation_layout.addWidget(log_button,2,1)
log_button.clicked.connect(lambda: active_equation.insert("log10("))
log_button.setStyleSheet(notation_button_style)

# absolute value button
abs_val_button = QPushButton("|x|")
notation_layout.addWidget(abs_val_button,2,2)
abs_val_button.clicked.connect(lambda: active_equation.add_absolute_value)
abs_val_button.setStyleSheet(notation_button_style)

# a button 
a_button = QPushButton("a")
notation_layout.addWidget(a_button,3,0)
a_button.clicked.connect(lambda: active_equation.insert("a"))  
a_button.setStyleSheet(notation_button_style)

# a^n button
a_pow_button = QPushButton("aⁿ")
notation_layout.addWidget(a_pow_button,3,1)
a_pow_button.clicked.connect(lambda: active_equation.add_a_power)
a_pow_button.setStyleSheet(notation_button_style)

# n root
n_root_button = QPushButton("ⁿ√")
notation_layout.addWidget(n_root_button,3,2)
n_root_button.clicked.connect(lambda: active_equation.add_n_root) 
n_root_button.setStyleSheet(notation_button_style)

# column width
notation_layout.setColumnStretch(0,1)
notation_layout.setColumnStretch(1,1)
notation_layout.setColumnStretch(2,1)

# row heights
notation_layout.setRowStretch(0,1)
notation_layout.setRowStretch(1,1)
notation_layout.setRowStretch(2,1)
notation_layout.setRowStretch(3,1)

notation_layout.setSpacing(5)

main_layout.addWidget(notation_panel, 1, 1)

# grid sizing

main_layout.setColumnStretch(0,3) # give graph & equation more space 
main_layout.setColumnStretch(1,2) # give right side less space 

main_layout.setRowStretch(0,5) # give top more space than bottom
main_layout.setRowStretch(1,2)

window.show()
app.exec()

# SOMETHING WRONG WITH EXPONENT BUTTON, FIX IT  
# SOMETHING WRONG WITH ABSOLUTE VALUE BUTTON, FIX IT