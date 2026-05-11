import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

x=sp.symbols('x')

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(6,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Series de Taylor')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('exp(x)')
        self.a=QLineEdit('0')
        self.n=QLineEdit('5')
        lay.addWidget(QLabel('f(x)')); lay.addWidget(self.expr)
        lay.addWidget(QLabel('Centro a')); lay.addWidget(self.a)
        lay.addWidget(QLabel('Orden n')); lay.addWidget(self.n)
        btn=QPushButton('Calcular Taylor')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.expr.text())
            a=float(self.a.text())
            n=int(self.n.text())
            serie=sp.series(expr,x,a,n+1).removeO()
            self.out.setText(f'Serie de Taylor:\n{serie}')
            self.plot(expr,serie)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,expr,serie):
        ax=self.canvas.ax; ax.clear()
        xs=np.linspace(-3,3,400)
        f=sp.lambdify(x,expr,'numpy')
        g=sp.lambdify(x,serie,'numpy')
        ax.plot(xs,f(xs),label='f(x)')
        ax.plot(xs,g(xs),label='Taylor')
        ax.grid(True); ax.legend(); ax.set_title('Aproximación de Taylor')
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())