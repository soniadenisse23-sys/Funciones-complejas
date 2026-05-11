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
        self.setWindowTitle('Calculadora - Teorema del Residuo')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('1/(z*(z-1))')
        self.z0=QLineEdit('0+0j')
        self.r=QLineEdit('2')
        lay.addWidget(QLabel('f(z)')); lay.addWidget(self.expr)
        lay.addWidget(QLabel('Centro contorno')); lay.addWidget(self.z0)
        lay.addWidget(QLabel('Radio')); lay.addWidget(self.r)
        btn=QPushButton('Calcular integral')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.expr.text())
            c=complex(self.z0.text())
            r=float(self.r.text())
            den=sp.denom(sp.together(expr))
            pts=sp.solve(sp.Eq(den,0),z)
            inside=[]; lines=[]; s=0
            for p in pts:
                pc=complex(sp.N(p))
                if abs(pc-c)<r:
                    res=sp.residue(expr,z,p)
                    s+=res; inside.append(pc)
                    lines.append(f'Res({p})={res}')
            integ=sp.simplify(2*sp.pi*sp.I*s)
            lines.append(f'Integral = {integ}')
            self.out.setText('\n'.join(lines))
            self.plot(c,r,inside)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,c,r,pts):
        ax=self.canvas.ax; ax.clear()
        th=np.linspace(0,2*np.pi,300)
        ax.plot(c.real+r*np.cos(th), c.imag+r*np.sin(th))
        for p in pts:
            ax.scatter([p.real],[p.imag],s=80)
        ax.set_title('Contorno y polos interiores')
        ax.axis('equal'); ax.grid(True)
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())