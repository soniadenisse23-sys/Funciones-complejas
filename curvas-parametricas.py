import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

t=sp.symbols('t', real=True)

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(6,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Curvas Paramétricas')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.xt=QLineEdit('cos(t)')
        self.yt=QLineEdit('sin(t)')
        self.a=QLineEdit('0')
        self.b=QLineEdit('2*pi')
        lay.addWidget(QLabel('x(t)')); lay.addWidget(self.xt)
        lay.addWidget(QLabel('y(t)')); lay.addWidget(self.yt)
        lay.addWidget(QLabel('t inicial')); lay.addWidget(self.a)
        lay.addWidget(QLabel('t final')); lay.addWidget(self.b)
        btn=QPushButton('Graficar curva')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            xexpr=sp.sympify(self.xt.text())
            yexpr=sp.sympify(self.yt.text())
            a=float(sp.N(sp.sympify(self.a.text())))
            b=float(sp.N(sp.sympify(self.b.text())))
            xsf=sp.lambdify(t,xexpr,'numpy')
            ysf=sp.lambdify(t,yexpr,'numpy')
            tt=np.linspace(a,b,500)
            X=xsf(tt); Y=ysf(tt)
            dx=sp.diff(xexpr,t); dy=sp.diff(yexpr,t)
            L=sp.integrate(sp.sqrt(dx**2+dy**2),(t,a,b))
            self.out.setText(f'x(t)={xexpr}\ny(t)={yexpr}\nLongitud = {sp.N(L)}')
            ax=self.canvas.ax; ax.clear(); ax.plot(X,Y)
            ax.scatter([X[0]],[Y[0]],s=50,label='Inicio')
            ax.set_title('Curva paramétrica'); ax.grid(True); ax.axis('equal'); ax.legend(); self.canvas.draw()
        except Exception as e:
            self.out.setText('Error: '+str(e))

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())