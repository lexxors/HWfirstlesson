from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_data=None):
        super(AddEditCoffeeForm, self).__init__()

        loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Add/Edit Coffee')

        self.coffee_data = coffee_data

        self.saveButton.clicked.connect(self.save_data)

        if coffee_data:
            self.fill_form()

    def fill_form(self):
        self.nameLineEdit.setText(self.coffee_data.get('name', ''))
        self.roastDegreeLineEdit.setText(self.coffee_data.get('roast_degree', ''))
        self.groundOrWholeLineEdit.setText(self.coffee_data.get('ground_or_whole', ''))
        self.flavorDescriptionLineEdit.setText(self.coffee_data.get('flavor_description', ''))
        self.priceLineEdit.setText(str(self.coffee_data.get('price', '')))
        self.packageVolumeLineEdit.setText(str(self.coffee_data.get('package_volume', '')))

    def save_data(self):
        name = self.nameLineEdit.text().strip()
        roast_degree = self.roastDegreeLineEdit.text().strip()
        ground_or_whole = self.groundOrWholeLineEdit.text().strip()
        flavor_description = self.flavorDescriptionLineEdit.text().strip()
        price = self.priceLineEdit.text().strip()
        package_volume = self.packageVolumeLineEdit.text().strip()

        if not name or not roast_degree or not ground_or_whole or not flavor_description or not price or not package_volume:
            QMessageBox.warning(self, 'Warning', 'Please fill in all fields.')
            return

        try:
            price = float(price)
            package_volume = int(package_volume)
        except ValueError:
            QMessageBox.warning(self, 'Warning', 'Invalid price or package volume. Please enter valid numbers.')
            return

        data = {
            'name': name,
            'roast_degree': roast_degree,
            'ground_or_whole': ground_or_whole,
            'flavor_description': flavor_description,
            'price': price,
            'package_volume': package_volume
        }

        if self.coffee_data:
            data['id'] = self.coffee_data['id']

        self.accept()
        return data
