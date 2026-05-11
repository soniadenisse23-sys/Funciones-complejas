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
        self.setWindowTitle('Calculadora - Teorema de Cauchy')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.f=QLineEdit('z**2+1')
        self.z0=QLineEdit('0+0j')
        self.r=QLineEdit('2')
        lay.addWidget(QLabel('f(z) holomorfa')); lay.addWidget(self.f)
        lay.addWidget(QLabel('Centro del contorno')); lay.addWidget(self.z0)
        lay.addWidget(QLabel('Radio')); lay.addWidget(self.r)
        btn=QPushButton('Aplicar teorema')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.f.text())
            den=sp.denom(sp.together(expr))
            sing=sp.solve(sp.Eq(den,0),z)
            c=complex(self.z0.text())
            r=float(self.r.text())
            inside=[]
            for s in sing:
                if abs(complex(sp.N(s))-c)<r:
                    inside.append(s)
            if len(inside)==0:
                msg='No hay singularidades dentro del contorno.\n∮ f(z) dz = 0'
            else:
                msg='Hay singularidades dentro del contorno:\n'+str(inside)
            self.out.setText(msg)
            self.plot(c,r,inside)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,c,r,pts):
        ax=self.canvas.ax; ax.clear()
        th=np.linspace(0,2*np.pi,300)
        ax.plot(c.real+r*np.cos(th), c.imag+r*np.sin(th))
        for p in pts:
            pc=complex(sp.N(p))
            ax.scatter([pc.real],[pc.imag],s=80)
        ax.set_xlabel('Re(z)'); ax.set_ylabel('Im(z)')
        ax.set_title('Contorno de Cauchy')
        ax.grid(True); ax.axis('equal'); self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
