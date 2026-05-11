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
        self.setWindowTitle('Serie de Laurent - Definición')
        self.resize(1000,800)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.f=QLineEdit('1/(z*(z-1))')
        self.z0=QLineEdit('0')
        self.n=QLineEdit('8')
        for lab,wd in [('f(z)',self.f),('Centro z0',self.z0),('Términos N',self.n)]:
            lay.addWidget(QLabel(lab)); lay.addWidget(wd)
        btn=QPushButton('Calcular y Graficar'); btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True); lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            f=sp.sympify(self.f.text())
            z0=sp.sympify(self.z0.text())
            N=int(self.n.text())
            serie=sp.series(f,z,z0,N).removeO()
            res=sp.residue(f,z,z0)
            self.out.setText(f'Serie de Laurent alrededor de z0={z0}:\n\n{serie}\n\nResiduo c_-1 = {res}')
            self.plot_graph(f,serie,z0)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot_graph(self,f,serie,z0):
        ax=self.canvas.ax; ax.clear()
        xs=np.linspace(-2,2,400)
        f1=sp.lambdify(z,f,'numpy')
        f2=sp.lambdify(z,serie,'numpy')
        y1=[]; y2=[]
        for x in xs:
            try: y1.append(complex(f1(x)))
            except: y1.append(np.nan+1j*np.nan)
            try: y2.append(complex(f2(x)))
            except: y2.append(np.nan+1j*np.nan)
        y1=np.array(y1,dtype=complex); y2=np.array(y2,dtype=complex)
        ax.plot(xs,np.real(y1),label='Re(f)')
        ax.plot(xs,np.real(y2),'--',label='Re(Laurent)')
        ax.axvline(float(sp.N(z0)),linestyle=':')
        ax.grid(True); ax.legend(); ax.set_title('Aproximación de Laurent sobre eje real')
        self.canvas.draw()

app=QApplication(sys.argv)
win=App(); win.show(); sys.exit(app.exec_())