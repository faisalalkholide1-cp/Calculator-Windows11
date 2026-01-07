import sys
import math
import ast
import operator

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit,
    QPushButton, QGridLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt


# -------- SAFE EVAL --------
allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}


def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        if isinstance(node, ast.UnaryOp):
            return allowed_operators[type(node.op)](
                eval_node(node.operand)
            )
        raise ValueError("Invalid Expression")

    tree = ast.parse(expr, mode='eval')
    return eval_node(tree.body)


# -------- UI --------
class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator Pro")
        self.setFixedSize(360, 520)
        self.build_ui()

    def build_ui(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet("""
            QLineEdit {
                background: rgba(30,30,30,180);
                color: white;
                font-size: 30px;
                padding: 15px;
                border-radius: 15px;
            }
        """)

        grid = QGridLayout()
        grid.setSpacing(10)

        buttons = [
            ('C',0,0),('√',0,1),('x²',0,2),('/',0,3),
            ('sin',1,0),('7',1,1),('8',1,2),('9',1,3),
            ('cos',2,0),('4',2,1),('5',2,2),('6',2,3),
            ('tan',3,0),('1',3,1),('2',3,2),('3',3,3),
            ('%',4,0),('0',4,1),('.',4,2),('=',4,3)
        ]

        for text, r, c in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(70,70)
            btn.clicked.connect(self.on_click)

            if text in ['+', '-', '*', '/', '=']:
                btn.setStyleSheet(self.op_style())
            elif text in ['sin','cos','tan','√','x²','%','C']:
                btn.setStyleSheet(self.func_style())
            else:
                btn.setStyleSheet(self.num_style())

            grid.addWidget(btn, r, c)

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.addWidget(self.display)
        layout.addLayout(grid)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #121212;")

    def on_click(self):
        t = self.sender().text()

        try:
            if t == 'C':
                self.display.clear()

            elif t == '=':
                result = safe_eval(self.display.text())
                self.display.setText(str(result))

            elif t == '√':
                self.display.setText(str(math.sqrt(float(self.display.text()))))

            elif t == 'x²':
                self.display.setText(str(float(self.display.text()) ** 2))

            elif t == '%':
                self.display.setText(str(float(self.display.text()) / 100))

            elif t in ['sin','cos','tan']:
                val = float(self.display.text())
                func = getattr(math, t)
                self.display.setText(str(func(math.radians(val))))

            else:
                self.display.setText(self.display.text() + t)

        except:
            self.display.setText("Error")

    def keyPressEvent(self, e):
        if e.text() in '0123456789.+-*/':
            self.display.setText(self.display.text() + e.text())
        elif e.key() == Qt.Key.Key_Return:
            self.on_click_equal()

    def num_style(self):
        return """
        QPushButton {
            background: #2a2a2a;
            color: white;
            font-size: 18px;
            border-radius: 35px;
        }
        QPushButton:hover { background: #3a3a3a; }
        """

    def op_style(self):
        return """
        QPushButton {
            background: #ff9500;
            color: white;
            font-size: 20px;
            border-radius: 35px;
        }
        """

    def func_style(self):
        return """
        QPushButton {
            background: #444;
            color: white;
            font-size: 16px;
            border-radius: 35px;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec())
