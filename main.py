import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidget, QListWidgetItem, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore

from main_window import Ui_MainWindow
from finish import Ui_Form
from value import Ui_Dialog

product_list = [{'img': 'kfc_icons/fries', 'food_name': 'French Fries', 'price': 54},
                {'img': 'kfc_icons/bucket', 'food_name': 'Bucket', 'price': 219},
                {'img': 'kfc_icons/pie', 'food_name': 'Raspberry-Blueberry Pie', 'price': 50},
                {'img': 'kfc_icons/partybox', 'food_name': 'Party Box', 'price': 124}
                ]

current_value = 0


class MenuWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listWidget.setViewMode(QListWidget.IconMode)
        for product in product_list:
            item = QListWidgetItem(QIcon(QPixmap(product['img'])), product['food_name'] + ', ' + str(product['price']))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)
        self.listWidget.itemChanged.connect(self.changed)
        self.order = dict()
        self.prices = dict()
        self.pushButton.clicked.connect(self.finish_order)

    def changed(self, item):
        pos, price = item.text().split(', ')
        self.prices[pos] = int(price)
        if item.checkState():
            d = Dialogue()
            d.show()
            d.exec()
            self.order[pos] = current_value
        else:
            self.order[item.text()] = 0

    def finish_order(self):
        total_price = 0
        text = ''
        for name in self.order.keys():
            if self.order[name] > 0:
                text += f'{name}       Кол-во {self.order[name]}    Сумма {self.prices[name] * self.order[name]}\n\n'
                total_price += self.prices[name] * self.order[name]
        text += f'Всего: {total_price}'
        self.receipt = Receipt()
        self.receipt.textBrowser.setText(text)
        self.receipt.show()


class Receipt(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Dialogue(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.get_value)
        self.buttonBox.rejected.connect(self.set_zero)

    def get_value(self):
        global current_value
        current_value = self.spinBox.value()

    def set_zero(self):
        global current_value
        current_value = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MenuWidget()
    form.show()
    sys.exit(app.exec())