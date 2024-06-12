import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox


class EmployeeListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Employee List App')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.btn_get_employees = QPushButton('Get Employees')
        self.btn_get_employees.clicked.connect(self.get_employees)
        layout.addWidget(self.btn_get_employees)

        self.setLayout(layout)

    def get_employees(self):
        try:
            headers = {
                'Accept': 'application/json'  # JSON形式のデータを要求するヘッダーを追加
            }
            response = requests.get('https://dummyjson.com/products', headers=headers)
            if response.status_code == 200:
                data = response.json()
                youa = data['products'][0]['title']
                self.list_widget.addItem(youa)
            else:
                QMessageBox.critical(self, 'Error', f"Failed to fetch data. Status Code: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmployeeListApp()
    window.show()
    sys.exit(app.exec_())

