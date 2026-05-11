import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

x,y=sp.symbols('x y', real=True)

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(6,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Funciones Armónicas')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('x**2 - y**2')
        lay.addWidget(QLabel('u(x,y)'))
        lay.addWidget(self.expr)
        btn=QPushButton('Analizar')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            u=sp.sympify(self.expr.text())
            uxx=sp.diff(u,x,2)
            uyy=sp.diff(u,y,2)
            lap=sp.simplify(uxx+uyy)
            armonica=(lap==0)
            txt=f'u(x,y)={u}\nuxx={uxx}\nuyy={uyy}\nΔu = uxx+uyy = {lap}\nArmónica: {armonica}'
            self.out.setText(txt)
            self.plot(u)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,u):
        ax=self.canvas.ax; ax.clear()
        xs=np.linspace(-2,2,120); ys=np.linspace(-2,2,120)
        X,Y=np.meshgrid(xs,ys)
        f=sp.lambdify((x,y),u,'numpy')
        Z=f(X,Y)
        c=ax.contourf(X,Y,Z,25)
        self.canvas.fig.colorbar(c, ax=ax)
        ax.set_xlabel('x'); ax.set_ylabel('y')
        ax.set_title('Mapa de u(x,y)')
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
