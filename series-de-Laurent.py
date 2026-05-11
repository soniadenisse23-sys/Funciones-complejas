import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

z=sp.symbols('z')

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(6,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Series de Laurent')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('1/(z*(z-1))')
        self.a=QLineEdit('0')
        self.n=QLineEdit('6')
        lay.addWidget(QLabel('f(z)')); lay.addWidget(self.expr)
        lay.addWidget(QLabel('Centro a')); lay.addWidget(self.a)
        lay.addWidget(QLabel('Términos')); lay.addWidget(self.n)
        btn=QPushButton('Calcular Laurent')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.expr.text())
            a=sp.sympify(self.a.text())
            n=int(self.n.text())
            serie=sp.series(expr,z,a,n).removeO()
            self.out.setText(f'Serie de Laurent/Taylor:\n{serie}')
            self.plot_annulus(a)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot_annulus(self,a):
        ax=self.canvas.ax; ax.clear()
        th=np.linspace(0,2*np.pi,300)
        r1,r2=0.5,2
        ax.plot(r1*np.cos(th)+float(sp.re(a)), r1*np.sin(th)+float(sp.re(a)))
        ax.plot(r2*np.cos(th)+float(sp.re(a)), r2*np.sin(th)+float(sp.re(a)))
        ax.set_title('Región anular típica de convergencia')
        ax.axis('equal'); ax.grid(True)
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())