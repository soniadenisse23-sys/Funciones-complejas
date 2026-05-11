import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

z=sp.symbols('z')
n=sp.symbols('n', integer=True, positive=True)

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(6,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Series de Potencias')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.term=QLineEdit('z**n/n')
        lay.addWidget(QLabel('Término general a_n(z)'))
        lay.addWidget(self.term)
        btn=QPushButton('Analizar convergencia')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.term.text())
            ratio=sp.simplify(sp.limit_abs(expr.subs(n,n+1)/expr, n, sp.oo))
            txt = f'Término general: a_n(z) = {sp.pretty(expr)}\n\nLímite de la razón: {sp.pretty(ratio)}\n\nCondición: converge cuando este valor < 1'
            self.out.setText(txt)
            self.plot(ratio)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,ratio):
        ax=self.canvas.ax; ax.clear()
        th=np.linspace(0,2*np.pi,400)
        r=1.0
        try:
            if ratio==abs(z): r=1
        except: pass
        x=r*np.cos(th); y=r*np.sin(th)
        ax.plot(x,y,label='Posible frontera |z|=R')
        ax.fill(x,y,alpha=0.3)
        ax.set_xlabel('Re(z)'); ax.set_ylabel('Im(z)')
        ax.set_title('Región típica de convergencia')
        ax.axis('equal'); ax.grid(True); ax.legend()
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
