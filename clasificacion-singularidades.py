import sys
import sympy as sp
import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

z=sp.symbols('z')

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure(figsize=(7,6))
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Clasificación de Singularidades Aisladas')
        self.resize(1000,800)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.f=QLineEdit('exp(1/z)')
        self.z0=QLineEdit('0')
        self.n=QLineEdit('8')
        for lab,wd in [('f(z)',self.f),('Punto z0',self.z0),('Orden expansión N',self.n)]:
            lay.addWidget(QLabel(lab)); lay.addWidget(wd)
        btn=QPushButton('Analizar y Graficar'); btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True); lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            f=sp.sympify(self.f.text())
            z0=sp.sympify(self.z0.text())
            N=int(self.n.text())
            serie=sp.series(f,z,z0,N)
            expr=serie.removeO()
            neg=[]
            for term in sp.Add.make_args(sp.expand(expr)):
                p=term.as_powers_dict().get(z-z0,0)
                try:
                    pv=int(p)
                    if pv<0: neg.append(pv)
                except: pass
            if len(neg)==0:
                tipo='Singularidad removible'
            else:
                orden=abs(min(neg))
                tipo=f'Polo de orden {orden}'
                if 'exp(1/' in str(f) or len(neg)>=N-2:
                    tipo='Singularidad esencial'
            self.out.setText(f'Serie de Laurent:\n{expr}\n\nClasificación: {tipo}')
            self.plot_graph(f,z0)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot_graph(self,f,z0):
        ax=self.canvas.ax; ax.clear()
        xs=np.linspace(-2,2,500)
        fun=sp.lambdify(z,f,'numpy')
        vals=[]
        for x in xs:
            try: vals.append(complex(fun(x)))
            except: vals.append(np.nan+1j*np.nan)
        vals=np.array(vals,dtype=complex)
        ax.plot(xs,np.real(vals),label='Re(f)')
        ax.plot(xs,np.imag(vals),label='Im(f)')
        ax.axvline(float(sp.N(z0)),linestyle=':')
        ax.grid(True); ax.legend(); ax.set_title('Comportamiento cerca de z0')
        self.canvas.draw()

app=QApplication(sys.argv)
win=App(); win.show(); sys.exit(app.exec_())
