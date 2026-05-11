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
        self.setWindowTitle('Calculadora - Singularidades Complejas')
        self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('sin(z)/z**3')
        lay.addWidget(QLabel('f(z)'))
        lay.addWidget(self.expr)
        btn=QPushButton('Analizar singularidades')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            expr=sp.sympify(self.expr.text())
            den=sp.denom(sp.together(expr))
            pts=sp.solve(sp.Eq(den,0),z)
            lines=[]
            for p in pts:
                kind='Singularidad'
                try:
                    lim=sp.limit((z-p)*expr,z,p)
                    if lim.is_finite and lim!=0:
                        kind='Polo simple'
                except: pass
                lines.append(f'z={p}: {kind}')
            if not pts:
                lines=['No se detectaron singularidades racionales.']
            self.out.setText('\n'.join(lines))
            self.plot(pts)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot(self,pts):
        ax=self.canvas.ax; ax.clear()
        ax.axhline(0); ax.axvline(0)
        for p in pts:
            pr=complex(sp.N(p))
            ax.scatter([pr.real],[pr.imag],s=80,label=str(p))
        ax.set_xlabel('Re(z)'); ax.set_ylabel('Im(z)')
        ax.set_title('Singularidades en el plano complejo')
        ax.grid(True); ax.legend()
        self.canvas.draw()

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
