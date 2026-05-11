import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

t=sp.symbols('t', real=True)
z=sp.symbols('z')

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(6,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Integrales sobre Curvas Complejas')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.f=QLineEdit('z**2')
        self.zt=QLineEdit('exp(I*t)')
        self.a=QLineEdit('0')
        self.b=QLineEdit('2*pi')
        lay.addWidget(QLabel('f(z)')); lay.addWidget(self.f)
        lay.addWidget(QLabel('z(t)')); lay.addWidget(self.zt)
        lay.addWidget(QLabel('t inicial')); lay.addWidget(self.a)
        lay.addWidget(QLabel('t final')); lay.addWidget(self.b)
        btn=QPushButton('Calcular integral')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            fexpr=sp.sympify(self.f.text())
            zexpr=sp.sympify(self.zt.text())
            a=float(sp.N(sp.sympify(self.a.text())))
            b=float(sp.N(sp.sympify(self.b.text())))
            dz=sp.diff(zexpr,t)
            integrand=sp.simplify(fexpr.subs(z,zexpr)*dz)
            val=sp.integrate(integrand,(t,a,b))
            self.out.setText(f'dz/dt = {dz}\nIntegrando = {integrand}\nIntegral = {sp.N(val)}')
            self.plot(zexpr,a,b)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,zexpr,a,b):
        ax=self.canvas.ax; ax.clear()
        tt=np.linspace(a,b,500)
        fun=sp.lambdify(t,zexpr,'numpy')
        Z=fun(tt)
        ax.plot(np.real(Z),np.imag(Z))
        ax.scatter([np.real(Z[0])],[np.imag(Z[0])],s=50,label='Inicio')
        ax.set_xlabel('Re(z)'); ax.set_ylabel('Im(z)')
        ax.set_title('Curva C en el plano complejo')
        ax.grid(True); ax.axis('equal'); ax.legend(); self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())