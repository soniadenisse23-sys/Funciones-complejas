import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

z = sp.symbols('z', complex=True)

def cauchy_integral_theorem(f, z0, radius, point):
    if abs(point - z0) >= radius:
        raise ValueError('El punto a debe estar dentro del contorno para aplicar Cauchy.')
    return sp.simplify(f.subs(z, point))

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora Gráfica - Integrales Complejas')
        self.resize(1000, 750)
        w = QWidget(); self.setCentralWidget(w)
        lay = QVBoxLayout(w)

        grid = QGridLayout()
        self.func = QLineEdit('sin(z)/z**3')  
        self.z0 = QLineEdit('0+0j')  
        self.r = QLineEdit('2')  
        self.a = QLineEdit('1+0j')  
        labels = [('f(z)',self.func),('Centro z0',self.z0),('Radio',self.r),('Punto a',self.a)]
        for i,(t,e) in enumerate(labels):
            grid.addWidget(QLabel(t), i,0); grid.addWidget(e,i,1)
        lay.addLayout(grid)

        btn = QPushButton('Calcular Integral de Cauchy')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)

        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.out.setText('Ejemplo cargado:\n f(z)=sin(z)/z**3\n z0=0+0j\n radio=2\n a=1+0j\n\nPulsa el botón para calcular.')
        self.canvas = Canvas(); lay.addWidget(self.canvas)

    def solve(self):
        try:
            f = sp.sympify(self.func.text())
            z0 = complex(self.z0.text())
            r = float(self.r.text())
            a = complex(self.a.text())
            res = cauchy_integral_theorem(f,z0,r,a)
            integral = sp.simplify(2*sp.pi*sp.I*res)
            txt = f'f(a) = {res}\n∮ f(z)/(z-a) dz = 2πi f(a) = {integral}'
            self.out.setText(txt)
            self.plot(z0,r,a)
        except Exception as e:
            self.out.setText('Error: '+str(e))

    def plot(self,z0,r,a):
        ax=self.canvas.ax; ax.clear()
        th=np.linspace(0,2*np.pi,500)
        x=z0.real + r*np.cos(th)
        y=z0.imag + r*np.sin(th)
        ax.plot(x,y,label='Contorno C')
        ax.scatter([a.real],[a.imag],s=80,label='a')
        ax.scatter([z0.real],[z0.imag],s=80,label='z0')
        ax.set_xlabel('Parte Real')
        ax.set_ylabel('Parte Imaginaria')
        ax.set_title('Plano Complejo')
        ax.grid(True)
        ax.axis('equal')
        ax.legend()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main(); win.show()
    sys.exit(app.exec_())
