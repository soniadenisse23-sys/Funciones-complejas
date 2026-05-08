import sys, cmath
import numpy as np
import sympy as sp
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
        super().__init__(); self.setWindowTitle('Funciones Elementales - Variable Compleja'); self.resize(1000,760)
        w=QWidget(); self.setCentralWidget(w); lay=QVBoxLayout(w)
        self.tabs=QTabWidget(); lay.addWidget(self.tabs)
        self.make_numbers(); self.make_polar(); self.make_functions()
    def make_numbers(self):
        tab=QWidget(); l=QVBoxLayout(tab)
        self.zin=QLineEdit('3+4j'); l.addWidget(QLabel('Número complejo z')); l.addWidget(self.zin)
        b=QPushButton('Calcular'); b.clicked.connect(self.calc_num); l.addWidget(b)
        self.out1=QTextEdit(); l.addWidget(self.out1)
        self.tabs.addTab(tab,'Números complejos')
    def calc_num(self):
        z=complex(self.zin.text()); self.out1.setText(f'z={z}\nRe={z.real}\nIm={z.imag}\n|z|={abs(z)}\nconjugado={z.conjugate()}')
    def make_polar(self):
        tab=QWidget(); l=QVBoxLayout(tab)
        self.zpol=QLineEdit('1+1j'); l.addWidget(QLabel('Número complejo z')); l.addWidget(self.zpol)
        b=QPushButton('Convertir a polar'); b.clicked.connect(self.calc_polar); l.addWidget(b)
        self.out2=QTextEdit(); l.addWidget(self.out2)
        self.canvas=Canvas(); l.addWidget(self.canvas)
        self.tabs.addTab(tab,'Forma polar')
    def calc_polar(self):
        z=complex(self.zpol.text()); r=abs(z); th=np.angle(z)
        self.out2.setText(f'z={z}\nr={r}\nθ={th} rad\nz = r(cosθ + i sinθ)')
        ax=self.canvas.ax; ax.clear(); ax.arrow(0,0,z.real,z.imag,head_width=0.1,length_includes_head=True)
        ax.scatter([z.real],[z.imag]); ax.grid(True); ax.axis('equal'); self.canvas.draw()
    def make_functions(self):
        tab=QWidget(); l=QVBoxLayout(tab)
        self.expr=QLineEdit('exp(z)'); self.val=QLineEdit('1+1j')
        l.addWidget(QLabel('f(z)')); l.addWidget(self.expr); l.addWidget(QLabel('Evaluar en z=')); l.addWidget(self.val)
        b=QPushButton('Evaluar función'); b.clicked.connect(self.calc_fun); l.addWidget(b)
        self.out3=QTextEdit(); l.addWidget(self.out3)
        self.canvas2=Canvas(); l.addWidget(self.canvas2)
        self.tabs.addTab(tab,'Funciones en variable compleja')
    def calc_fun(self):
        try:
            expr = sp.sympify(self.expr.text())
            val = complex(self.val.text())
            res = sp.N(expr.subs(z, val))
            self.out3.setText(f'f(z)={expr}\nf({val})={res}')
            xs = np.linspace(-2, 2, 400)
            fnum = sp.lambdify(z, expr, modules=['numpy'])
            ys = np.asarray(fnum(xs), dtype=np.complex128)
            ax = self.canvas2.ax
            ax.clear()
            ax.plot(np.real(ys), np.imag(ys), linewidth=2, label='Trayectoria f(x)')
            ax.scatter([float(np.real(ys[0]))], [float(np.imag(ys[0]))], s=40, label='Inicio')
            ax.set_xlabel('Re(f)')
            ax.set_ylabel('Im(f)')
            ax.set_title('Imagen en el plano complejo')
            ax.grid(True)
            ax.axis('equal')
            ax.legend()
            self.canvas2.draw()
        except Exception as e:
            self.out3.setText('Error: ' + str(e))

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
