import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QMessageBox

from ui.LoadDialog_ui import Ui_LoadDialog

class LoadDialog(QDialog, Ui_LoadDialog):
    Nifti_Signal = Signal(str, str)
    Dicom_Signal = Signal(str)
    IMA_Signal = Signal(str)
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.config()

    def config(self) -> None:
        self.load_state: str = self.comboBox.currentText()
        self.setWindowTitle("导入文件")

    @Slot(str)
    def on_comboBox_currentTextChanged(self, text) -> None:
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.load_state = text

    @Slot(bool)
    def on_btnSearch_clicked(self, clicked) -> None:
        data_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "NIfTI Files (*.nii *.nii.gz)")
        if data_path:
            self.lineEdit.setText(data_path)

    @Slot(bool)
    def on_btnSearch_2_clicked(self, clicked) -> None:
        data_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "NIfTI Files (*.nii *.nii.gz)")
        if data_path:
            self.lineEdit_2.setText(data_path)

    @Slot(bool)
    def on_btnSearch_3_clicked(self, clicked) -> None:
        data_path: str = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if data_path:
            self.lineEdit_3.setText(data_path)
    
    @Slot(bool)
    def on_btnSearch_4_clicked(self, clicked) -> None:
        data_path: str = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if data_path:
            self.lineEdit_4.setText(data_path)
            
    @Slot(bool)
    def on_btnCancel_clicked(self, clicked) -> None:
        self.close()

    @Slot(bool)
    def on_btnLoad_clicked(self, clicked) -> None:
        if self.load_state == "NIfTI":
            if self.lineEdit.text() == "" or self.lineEdit_2.text() == "":
                QMessageBox.warning(self, "提示", "请选择文件", QMessageBox.Ok)
                return
            else:
                self.Nifti_Signal.emit(self.lineEdit.text(), self.lineEdit_2.text())

        elif self.load_state == "DICOM":
            if self.lineEdit_3.text() == "":
                QMessageBox.warning(self, "提示", "请选择文件夹", QMessageBox.Ok)
                return
            else:
                self.Dicom_Signal.emit(self.lineEdit_3.text())

        elif self.load_state == "IMA":
            if self.lineEdit_4.text() == "":
                QMessageBox.warning(self, "提示", "请选择文件夹", QMessageBox.Ok)
                return
            else:
                self.IMA_Signal.emit(self.lineEdit_4.text())
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoadDialog()
    ui.show()
    sys.exit(app.exec_())