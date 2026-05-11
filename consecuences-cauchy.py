import sys
import sympy as sp
from PyQt5.QtWidgets import *

z=sp.symbols('z')

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora - Consecuencias del Teorema de Cauchy')
        self.resize(900,700)
        w=QWidget(); self.setCentralWidget(w)
        lay=QVBoxLayout(w)
        self.expr=QLineEdit('exp(z)')
        self.a=QLineEdit('0')
        self.n=QLineEdit('3')
        lay.addWidget(QLabel('f(z)')) ; lay.addWidget(self.expr)
        lay.addWidget(QLabel('Evaluar en a')) ; lay.addWidget(self.a)
        lay.addWidget(QLabel('Orden derivada n')) ; lay.addWidget(self.n)
        btn=QPushButton('Analizar consecuencias')
        btn.clicked.connect(self.solve)
        lay.addWidget(btn)
        self.out=QTextEdit(); self.out.setReadOnly(True); lay.addWidget(self.out)
    def solve(self):
        try:
            f=sp.sympify(self.expr.text())
            a=sp.sympify(self.a.text())
            n=int(self.n.text())
            deriv=sp.diff(f,z,n)
            val=sp.simplify(deriv.subs(z,a))
            poly = f.is_polynomial(z)
            lines=[]
            lines.append(f'f^( {n} )(z) = {deriv}')
            lines.append(f'f^( {n} )({a}) = {val}')
            lines.append('Consecuencia 1: holomorfa => infinitamente derivable.')
            lines.append('Consecuencia 2: existe serie de Taylor local.')
            lines.append('Consecuencia 3: principio de identidad (si coincide en un conjunto con acumulación).')
            if poly:
                lines.append('Consecuencia extra: al ser polinomio, es entera.')
            self.out.setText('\n\n'.join(lines))
        except Exception as e:
            self.out.setText('Error: '+str(e))

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=App(); win.show()
    sys.exit(app.exec_())
