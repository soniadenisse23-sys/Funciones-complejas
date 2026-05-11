import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QPushButton,QTextEdit)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

z=sp.symbols('z', complex=True)

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(5,5))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora Gráfica Compleja')
        self.resize(900,700)
        central=QWidget(); self.setCentralWidget(central)
        layout=QVBoxLayout(central)
        form=QHBoxLayout()
        self.func=QLineEdit('sin(z)/z**3')
        self.center=QLineEdit('0+0j')
        self.radius=QLineEdit('2')
        self.point=QLineEdit('1+0j')
        for t,w in [('f(z):',self.func),('z0:',self.center),('r:',self.radius),('a:',self.point)]:
            form.addWidget(QLabel(t)); form.addWidget(w)
        layout.addLayout(form)
        btn=QPushButton('Calcular y Graficar'); btn.clicked.connect(self.run)
        layout.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        layout.addWidget(self.out)
        self.canvas=MplCanvas(); layout.addWidget(self.canvas)
    def run(self):
        try:
            f=sp.sympify(self.func.text())
            z0=complex(self.center.text())
            r=float(self.radius.text())
            a=complex(self.point.text())
            if abs(a-z0)>=r:
                raise ValueError('El punto a debe estar dentro del contorno.')
            res=sp.simplify(f.subs(z,a))
            self.out.setText(f'f(a) según Cauchy = {res}')
            self.plot(z0,r,a)
        except Exception as e:
            self.out.setText(f'Error: {e}')
    def plot(self,z0,r,a):
        self.canvas.ax.clear()
        th=np.linspace(0,2*np.pi,400)
        x=z0.real+r*np.cos(th); y=z0.imag+r*np.sin(th)
        ax=self.canvas.ax
        ax.plot(x,y,label='Contorno')
        ax.scatter([a.real],[a.imag],label='a')
        ax.scatter([z0.real],[z0.imag],label='z0')
        ax.set_xlabel('Real'); ax.set_ylabel('Imaginaria')
        ax.grid(True); ax.axis('equal'); ax.legend()
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
