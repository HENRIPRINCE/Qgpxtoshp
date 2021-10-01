# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_gpx_shp.ui'
#
# Created: Thu Apr 27 16:02:43 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_gpx_shp(object):
    def setupUi(self, gpx_shp):
        gpx_shp.setObjectName(_fromUtf8("gpx_shp"))
        gpx_shp.resize(460, 260)
        self.grb_Layer = QtGui.QGroupBox(gpx_shp)
        self.grb_Layer.setGeometry(QtCore.QRect(10, 30, 431, 41))
        self.grb_Layer.setTitle(_fromUtf8(""))
        self.grb_Layer.setObjectName(_fromUtf8("grb_Layer"))
        self.btn_RepgpxOuvrir = QtGui.QPushButton(self.grb_Layer)
        self.btn_RepgpxOuvrir.setGeometry(QtCore.QRect(350, 10, 75, 23))
        self.btn_RepgpxOuvrir.setObjectName(_fromUtf8("btn_RepgpxOuvrir"))
        self.rep_travail = QtGui.QTextEdit(self.grb_Layer)
        self.rep_travail.setGeometry(QtCore.QRect(10, 10, 331, 21))
        self.rep_travail.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.rep_travail.setAcceptDrops(True)
        self.rep_travail.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rep_travail.setLineWidth(1)
        self.rep_travail.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rep_travail.setObjectName(_fromUtf8("rep_travail"))
        self.label_19 = QtGui.QLabel(gpx_shp)
        self.label_19.setGeometry(QtCore.QRect(10, 10, 211, 16))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.grb_Echelle = QtGui.QGroupBox(gpx_shp)
        self.grb_Echelle.setGeometry(QtCore.QRect(10, 80, 431, 51))
        self.grb_Echelle.setObjectName(_fromUtf8("grb_Echelle"))
        self.label_5 = QtGui.QLabel(self.grb_Echelle)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lbl_Events = QtGui.QLabel(self.grb_Echelle)
        self.lbl_Events.setGeometry(QtCore.QRect(180, 20, 191, 20))
        self.lbl_Events.setObjectName(_fromUtf8("lbl_Events"))
        self.groupBox = QtGui.QGroupBox(gpx_shp)
        self.groupBox.setGeometry(QtCore.QRect(10, 150, 431, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.rep_shpSave = QtGui.QTextEdit(self.groupBox)
        self.rep_shpSave.setGeometry(QtCore.QRect(10, 40, 331, 21))
        self.rep_shpSave.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.rep_shpSave.setAcceptDrops(True)
        self.rep_shpSave.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rep_shpSave.setLineWidth(1)
        self.rep_shpSave.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rep_shpSave.setObjectName(_fromUtf8("rep_shpSave"))
        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.btn_RepshpSave = QtGui.QPushButton(self.groupBox)
        self.btn_RepshpSave.setGeometry(QtCore.QRect(350, 40, 75, 23))
        self.btn_RepshpSave.setObjectName(_fromUtf8("btn_RepshpSave"))
        self.chbxCanvas = QtGui.QCheckBox(self.groupBox)
        self.chbxCanvas.setGeometry(QtCore.QRect(10, 70, 141, 20))
        self.chbxCanvas.setChecked(True)
        self.chbxCanvas.setObjectName(_fromUtf8("chbxCanvas"))
        self.btn_Executer = QtGui.QPushButton(self.groupBox)
        self.btn_Executer.setGeometry(QtCore.QRect(350, 70, 75, 23))
        self.btn_Executer.setObjectName(_fromUtf8("btn_Executer"))

        self.retranslateUi(gpx_shp)
        QtCore.QMetaObject.connectSlotsByName(gpx_shp)

    def retranslateUi(self, gpx_shp):
        gpx_shp.setWindowTitle(_translate("gpx_shp", "REGROUPEMENT & CONVERTIR GPX en SHP", None))
        self.btn_RepgpxOuvrir.setText(_translate("gpx_shp", "Parcourir", None))
        self.label_19.setText(_translate("gpx_shp", "Selectionner lerepertoire de travail", None))
        self.grb_Echelle.setTitle(_translate("gpx_shp", "Informations:", None))
        self.label_5.setText(_translate("gpx_shp", "Nombre des fichiers gpx trouvé(s)", None))
        self.lbl_Events.setText(_translate("gpx_shp", "0", None))
        self.groupBox.setTitle(_translate("gpx_shp", "Fichier de sortie (shapefile)", None))
        self.label_15.setText(_translate("gpx_shp", "Selectionner le fichier de sortie", None))
        self.btn_RepshpSave.setText(_translate("gpx_shp", "Parcourir", None))
        self.chbxCanvas.setText(_translate("gpx_shp", "Ajouter au canvas", None))
        self.btn_Executer.setText(_translate("gpx_shp", "Executer", None))

