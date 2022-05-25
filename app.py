from controller import controlador
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = controlador()
    ventana.show()
    sys.exit(app.exec_())