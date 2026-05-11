import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

z = sp.symbols('z')

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora Gráfica - Límites Complejos')
        self.resize(1000,760)
        w = QWidget(); self.setCentralWidget(w)
        lay = QVBoxLayout(w)
        self.expr = QLineEdit('(z**2-1)/(z-1)')
        self.point = QLineEdit('1')
        lay.addWidget(QLabel('f(z)'))
        lay.addWidget(self.expr)
        lay.addWidget(QLabel('Lim z→a, a='))
        lay.addWidget(self.point)
        btn = QPushButton('Calcular límite')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas = Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr = sp.sympify(self.expr.text())
            a = complex(self.point.text())
            lim = sp.limit(expr, z, a)
            self.out.setText(f'lim z→{a} {expr} = {lim}')
            self.plot_paths(expr,a)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot_paths(self,expr,a):
        ax=self.canvas.ax; ax.clear()
        t=np.linspace(0.05,2,200)
        fnum=sp.lambdify(z,expr,'numpy')
        p1=a+t
        p2=a+1j*t
        y1=fnum(p1)
        y2=fnum(p2)
        ax.plot(np.real(y1),np.imag(y1),label='Camino real')
        ax.plot(np.real(y2),np.imag(y2),label='Camino imaginario')
        ax.set_xlabel('Re(f)'); ax.set_ylabel('Im(f)')
        ax.set_title('Aproximación al límite por caminos')
        ax.grid(True); ax.axis('equal'); ax.legend()
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
