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
        self.setWindowTitle('Calculadora - Fórmula Integral de Cauchy')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.f=QLineEdit('exp(z)')
        self.a=QLineEdit('1')
        self.z0=QLineEdit('0+0j')
        self.r=QLineEdit('2')
        lay.addWidget(QLabel('f(z)')); lay.addWidget(self.f)
        lay.addWidget(QLabel('Punto a')); lay.addWidget(self.a)
        lay.addWidget(QLabel('Centro contorno')); lay.addWidget(self.z0)
        lay.addWidget(QLabel('Radio')); lay.addWidget(self.r)
        btn=QPushButton('Aplicar fórmula')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.f.text())
            a=complex(self.a.text())
            c=complex(self.z0.text())
            r=float(self.r.text())
            if abs(a-c)>=r:
                raise ValueError('a debe estar dentro del contorno')
            fa=sp.N(expr.subs(z,a))
            integ=sp.simplify(2*sp.pi*sp.I*expr.subs(z,a))
            txt=f'f(a) = {fa}\n∮ f(z)/(z-a) dz = {integ}'
            self.out.setText(txt)
            self.plot(c,r,a)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,c,r,a):
        ax=self.canvas.ax; ax.clear()
        th=np.linspace(0,2*np.pi,300)
        ax.plot(c.real+r*np.cos(th), c.imag+r*np.sin(th))
        ax.scatter([a.real],[a.imag],s=80,label='a')
        ax.set_xlabel('Re(z)'); ax.set_ylabel('Im(z)')
        ax.set_title('Contorno y punto interior')
        ax.grid(True); ax.axis('equal'); ax.legend(); self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
