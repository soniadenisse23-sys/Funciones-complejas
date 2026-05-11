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
        self.setWindowTitle('Teorema de Taylor Complejo')
        self.resize(1000,800)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.f=QLineEdit('exp(z)')
        self.z0=QLineEdit('0')
        self.n=QLineEdit('6')
        self.rho=QLineEdit('1')
        for lab,widget in [('f(z)',self.f),('Centro z0',self.z0),('Orden N',self.n),('Radio ρ del contorno',self.rho)]:
            lay.addWidget(QLabel(lab)); lay.addWidget(widget)
        btn=QPushButton('Calcular y Graficar'); btn.clicked.connect(self.solve); lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True); lay.addWidget(self.out)
        self.canvas=Canvas(); lay.addWidget(self.canvas)
    def solve(self):
        try:
            f=sp.sympify(self.f.text())
            z0=complex(self.z0.text())
            N=int(self.n.text())
            rho=float(self.rho.text())
            S=0; lines=[]
            for k in range(N+1):
                ak=sp.simplify(sp.diff(f,z,k).subs(z,z0)/sp.factorial(k))
                S += ak*(z-z0)**k
                lines.append(f'a_{k} = {ak}')
            lines.append('\nSerie de Taylor:')
            lines.append(str(sp.expand(S)))
            self.out.setText('\n'.join(lines))
            self.plot_graph(f,S,z0,rho)
        except Exception as e:
            self.out.setText('Error: '+str(e))
    def plot_graph(self,f,S,z0,rho):
        ax=self.canvas.ax; ax.clear()
        xs=np.linspace(z0.real-2*rho,z0.real+2*rho,400)
        f1=sp.lambdify(z,f,'numpy'); f2=sp.lambdify(z,S,'numpy')
        y1=np.array(f1(xs),dtype=complex)
        y2=np.array(f2(xs),dtype=complex)
        ax.plot(xs,np.real(y1),label='Re(f)')
        ax.plot(xs,np.real(y2),'--',label='Re(Taylor)')
        ax.axvline(z0.real,linestyle=':')
        circx=z0.real+rho*np.cos(np.linspace(0,2*np.pi,200))
        circy=z0.imag+rho*np.sin(np.linspace(0,2*np.pi,200))
        ax2=self.canvas.fig.add_axes([0.62,0.58,0.25,0.25])
        ax2.clear(); ax2.plot(circx,circy); ax2.scatter([z0.real],[z0.imag]); ax2.set_title('Contorno γ'); ax2.axis('equal')
        ax.grid(True); ax.legend(); ax.set_title('Aproximación de Taylor sobre eje real')
        self.canvas.draw()

app=QApplication(sys.argv)
win=App(); win.show(); sys.exit(app.exec_())