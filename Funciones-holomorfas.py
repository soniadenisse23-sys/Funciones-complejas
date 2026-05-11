import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

x,y = sp.symbols('x y', real=True)
z = sp.symbols('z')

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Funciones Holomorfas')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('z**2')
        lay.addWidget(QLabel('f(z)'))
        lay.addWidget(self.expr)
        btn=QPushButton('Analizar holomorfía')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.expr.text())
            wexpr=expr.subs(z, x+sp.I*y).expand(complex=True)
            u=sp.re(wexpr); v=sp.im(wexpr)
            ux=sp.diff(u,x); uy=sp.diff(u,y)
            vx=sp.diff(v,x); vy=sp.diff(v,y)
            cr1=sp.simplify(ux-vy)
            cr2=sp.simplify(uy+vx)
            holo = (cr1==0 and cr2==0)
            txt=f'u(x,y)={u}\nv(x,y)={v}\nux={ux}, uy={uy}\nvx={vx}, vy={vy}\nCR1=ux-vy={cr1}\nCR2=uy+vx={cr2}\nHolomorfa: {holo}'
            self.out.setText(txt)
            self.plot(u)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,u):
        ax=self.canvas.ax; ax.clear()
        xs=np.linspace(-2,2,100); ys=np.linspace(-2,2,100)
        X,Y=np.meshgrid(xs,ys)
        fun=sp.lambdify((x,y),u,'numpy')
        Z=fun(X,Y)
        c=ax.contourf(X,Y,Z,20)
        self.canvas.fig.colorbar(c, ax=ax)
        ax.set_title('Parte real u(x,y)')
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())