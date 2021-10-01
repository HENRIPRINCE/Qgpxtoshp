# -*- coding: utf-8 -*-

from PyQt4.QtSql import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *




import sys
import os
import os, re
import os.path
import math
import psycopg2
import datetime
import platform
import socket
import processing
import qgis.utils

from qgis import *
from qgis.core import *
from qgis.gui import *



class Class_objet(object):
	def __init__(self, mon_UI):
		self.db = QSqlDatabase.addDatabase("QPSQL")
		self.mon_UI = mon_UI
		#--pour treeView
		self.model = QStandardItemModel()
		self.model.setHorizontalHeaderLabels(["DATA_SERVER"])
	
	def exe_sql(self,monSQL):
		sig_host = "172.16.0.230"
		sig_port="5432"
		role_carte = "cnx_carte"
		mdp_carte = "sigbienipmcarte"
		bd_charger = "bd_locale_ipm"
		
		#db = QSqlDatabase.addDatabase("QPSQL")
		self.db.setHostName(sig_host)
		self.db.setPort(int(sig_port))
		self.db.setDatabaseName(bd_charger)
		self.db.setUserName(role_carte)
		self.db.setPassword(mdp_carte)
		self.db.open()
		query = self.db.exec_(monSQL)
		
		return query
		
	def login_ici(self):
		Membres = 0
		query = self.exe_sql("""select * from tbl_cnx where son_login  = '""" + self.mon_UI.son_login.toPlainText() + """' and mdp = '""" + self.mon_UI.son_mdp.text() + """'""")
		while query.next():
				Membres += 1
		
		if Membres > 0:
			self.mon_UI.son_statut.setText('ON_LINE')
			self.mon_UI.btn_Ajout.setEnabled(True)
			self.mon_UI.btn_Annule_Select.setEnabled(True)
			QtGui.QMessageBox.information(QWidget(), 'Message', "Vous êtes connecté".decode("utf-8"))
		else:
			self.mon_UI.son_statut.setText('HORS_LINE')
			self.mon_UI.btn_Ajout.setDisabled(True)
			self.mon_UI.btn_Annule_Select.setDisabled(True)
			QtGui.QMessageBox.information(QWidget(), 'Message', "Vous n'est pas connecté!".decode("utf-8"))
			
	
	def click_radio1(self):
		try:
			# pour les données spatial
			self.mon_UI.liste_base.clear()
			#pour treeView
			data_vide =[]
			self.mon_UI.tV_table.clearSelection()
			self.addItems(self.model, data_vide)
			self.mon_UI.tV_table.setModel(self.model)
			self.model.setHorizontalHeaderLabels(['DATA_SERVER'])
			
			txt_statut = self.mon_UI.son_statut.toPlainText()
			self.mon_UI.base_encours.setText('spatial')
		
			if txt_statut == 'ON_LINE':
				query = self.exe_sql("""select nom_base, type_base from tbl_all_base where type_base='spatial'""")
				while query.next():
					record = query.record()
					self.mon_UI.liste_base.addItem(str(record.field('nom_base').value()))
					
		except:
			pass
			
	
	def click_radio2(self):
		try:
			# pour les données non spatial
			self.mon_UI.liste_base.clear()
			#pour treeView
			data_vide =[]
			self.mon_UI.tV_table.clearSelection()
			self.addItems(self.model, data_vide)
			self.mon_UI.tV_table.setModel(self.model)
			self.model.setHorizontalHeaderLabels(['DATA_SERVER'])
			
			txt_statut = self.mon_UI.son_statut.toPlainText()
			self.mon_UI.base_encours.setText('non_spatial')

			if txt_statut == 'ON_LINE':
				query = self.exe_sql("""select nom_base, type_base from tbl_all_base where type_base='non_spatial'""")
				while query.next():
					record = query.record()
					self.mon_UI.liste_base.addItem(str(record.field('nom_base').value()))
					
		except:
			pass
		
		
	
	def chargertable_fonc(self):
		sig_host = "172.16.0.230"
		sig_port = "5432"
		role_cnx = "cnx_user"
		mdp_cnx = "sigDN01072007ipm"
		try:
			val_base_encours = str(self.mon_UI.base_encours.toPlainText())
			if self.mon_UI.liste_base.count()>0:
				val_liste_base = str(self.mon_UI.liste_base.currentItem().text())
			
			#self.mon_UI.liste_table.clear()
			self.db.setHostName(sig_host)
			self.db.setPort(int(sig_port))
			self.db.setDatabaseName(val_liste_base)
			self.db.setUserName(role_cnx)
			self.db.setPassword(mdp_cnx)
			self.db.open()
			if val_base_encours=='spatial':
				#-----------------------------Debut traitement-----------------------------#
				query = self.db.exec_("""select schemaname from pg_stat_all_tables group by schemaname having schemaname not in ('information_schema','pg_catalog', 'pg_toast', 'public', 'topology') order by schemaname""")
				reniny = []
				zanany= []
				while query.next():
					zanany= []
					record = query.record()
					query2 = self.db.exec_("""select schemaname, relname from pg_stat_all_tables group by schemaname, relname having schemaname = '"""+ str(record.field('schemaname').value()) + """'""")
					while query2.next():
						record2 = query2.record()
						if str(record2.field('schemaname').value()) =='public':
							tbl_ajout = str(record2.field('relname').value())
						else:
							tbl_ajout = str(record2.field('schemaname').value()) +'.'+ str(record2.field('relname').value())
							
						#zanany.append(tuple([str(record2.field('relname').value()), []]))
						zanany.append(tuple([tbl_ajout, []]))

					reniny.append(tuple([ str(record.field('schemaname').value()) ,  zanany]))
				
				data = reniny
				self.addItems(self.model, data)
				self.mon_UI.tV_table.setModel(self.model)
				self.model.setHorizontalHeaderLabels([val_liste_base])
				#-----------------------------Fin traitement-----------------------------#
			
			if val_base_encours=='non_spatial':
				#-----------------------------Debut traitement-----------------------------#
				query = self.db.exec_("""select schemaname from pg_stat_all_tables group by schemaname having schemaname not in ('information_schema','pg_catalog', 'pg_toast', 'topology') order by schemaname""")
				reniny = []
				zanany= []
				nom_schema=''
				while query.next():
					zanany= []
					record = query.record()
					query2 = self.db.exec_("""select schemaname, relname from pg_stat_all_tables group by schemaname, relname having schemaname = '"""+ str(record.field('schemaname').value()) + """'""")
					while query2.next():
						record2 = query2.record()
						if str(record2.field('schemaname').value()) =='public':
							tbl_ajout = str(record2.field('relname').value())
						else:
							tbl_ajout = str(record2.field('schemaname').value()) +'.'+ str(record2.field('relname').value())
							
						#zanany.append(tuple([str(record2.field('relname').value()), []]))
						zanany.append(tuple([tbl_ajout, []]))

					if str(record.field('schemaname').value()) =='public':
						nom_schema ='Tables'
					else:
						nom_schema = str(record.field('schemaname').value())
						
					reniny.append(tuple([ nom_schema ,  zanany]))
					#reniny.append(tuple([ str(record.field('schemaname').value()) ,  zanany]))
				
				data = reniny
				self.addItems(self.model, data)
				self.mon_UI.tV_table.setModel(self.model)
				self.model.setHorizontalHeaderLabels([val_liste_base])
				#-----------------------------Fin traitement-----------------------------#
				
				#all views
				#-----------------------------Debut traitement-----------------------------#
				query_2 = self.db.exec_("""select schemaname from pg_views group by schemaname having schemaname not in ('information_schema','pg_catalog', 'pg_toast', 'topology') order by  schemaname """)
				reniny = []
				zanany= []
				nom_schema_Vue=''
				while query_2.next():
					zanany= []
					record = query_2.record()
					query2 = self.db.exec_("""select schemaname, viewname from pg_views group by schemaname, viewname having schemaname = '"""+ str(record.field('schemaname').value()) + """'""")
					while query2.next():
						record2 = query2.record()
						if str(record2.field('schemaname').value()) =='public':
							tbl_ajout = str(record2.field('viewname').value())
						else:
							tbl_ajout = str(record2.field('schemaname').value()) +'.'+ str(record2.field('viewname').value())
							
						#zanany.append(tuple([str(record2.field('viewname').value()), []]))
						zanany.append(tuple([tbl_ajout, []]))

					if str(record.field('schemaname').value()) =='public':
						nom_schema_Vue ='Vues'
					else:
						nom_schema_Vue = str(record.field('schemaname').value())
						
					reniny.append(tuple([ nom_schema_Vue ,  zanany]))
					#reniny.append(tuple([ str(record.field('schemaname').value()) ,  zanany]))
				
				data = reniny
				self.addItems(self.model, data)
				self.mon_UI.tV_table.setModel(self.model)
				self.model.setHorizontalHeaderLabels([val_liste_base])
				#-----------------------------Fin traitement-----------------------------#
				
				
		except:
			pass
			
	
	def addItems(self, parent, elements):
		for text, children in elements:
			item = QStandardItem(text)
			parent.appendRow(item)
			if children:
				self.addItems(item, children)
	
	def on_treeView_clicked_fonc(self):
		"""
		isanZananySeleky=0
		#for index in self.ui.tV_table.selectedIndexes():
		for index in self.ui.tV_table.selectionModel().selectedIndexes():
			isanZaza=0
			Zanany = index.model().itemFromIndex(index).rowCount()
			for isa in range (0, Zanany):
				isanZaza +=1
				
			if isanZaza == 0:
				isanZananySeleky +=1
				fileName = index.model().itemFromIndex(index).text()
				#QtGui.QMessageBox.information(self, 'Message',  fileName)
			else:
				fileParent = index.model().itemFromIndex(index).text()
				#QtGui.QMessageBox.information(self, 'Message',  fileParent)
				self.mon_UI.tV_table.clearSelection()
			
		QtGui.QMessageBox.information(self, 'isany',  str(isanZananySeleky))
		"""
		
	def ajouter_fonc(self, schema_table):
		sig_host = "172.16.0.230"
		sig_port="5432"
		role_cnx = "cnx_user"
		mdp_cnx = "sigDN01072007ipm"
		role_carte = "cnx_carte"
		mdp_carte = "sigbienipmcarte"
		bd_charger = "bd_locale_ipm"
		tbl_sig = "tbl_logged_qgis"
		valSelect =''
		sql=''
		try:
			#QtGui.QMessageBox.information(QWidget(), 'fichier :', schema_table)
			#all informations
			mon_ordi = str(platform.platform()) + ' - ' + str(platform.machine())
			izao = datetime.datetime.now()
			daty = str(izao.year) + '-' + str(izao.month) + '-' + str(izao.day)
			ora = str(izao.hour) + ':' + str(izao.minute) + ':' + str(izao.second)
			q_version = qgis.utils.QGis.QGIS_VERSION
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("172.16.0.230",80))
			son_ip = str(s.getsockname()[0])
			s.close()
			#informations a chargrer
			txt_login = self.mon_UI.son_login.toPlainText()
			Nom_base = str(self.mon_UI.liste_base.currentItem().text())
			val_base_encours = str(self.mon_UI.base_encours.toPlainText())
			#charger la couche
			uri = QgsDataSourceURI()
			if val_base_encours=='spatial': 
				con = None
				con = psycopg2.connect("dbname='" + bd_charger + "' user='" + role_carte+ "' password='" + mdp_carte + "' host='" + sig_host + "' port='"+ sig_port +"'")
				iSchema,iTable = schema_table.split('.')
				#stocker informations client dans la base
				sql ="""INSERT INTO """ + tbl_sig + """ VALUES('""" + txt_login +"""','""" + daty + """', '""" + ora + """', '""" + Nom_base + """', '""" + iSchema + """', '"""+ iTable + """', '""" + son_ip +"""','"""+ mon_ordi + """', '""" + q_version + """', 'spatial')"""
				cur = con.cursor()
				cur.execute(sql)
				con.commit()
				cur.close()
				#charger la couche
				uri.setConnection(sig_host,sig_port, Nom_base, role_cnx ,mdp_cnx, QgsDataSourceURI.SSLdisable)
				uri.setDataSource(iSchema,iTable,"geom","", "id_0")
				uri.setSrid("4326")
				vlayer = QgsVectorLayer(uri.uri(),iTable,"postgres")
				QgsMapLayerRegistry.instance().addMapLayer(vlayer)
				#Fermer base					
				con.close()
				
			if val_base_encours=='non_spatial': 
				#geom_column = ''
				geom_column = None
				con = None
				con = psycopg2.connect("dbname='" + bd_charger + "' user='" + role_carte + "' password='" + mdp_carte + "' host='" + sig_host + "' port='"+ sig_port +"'")
				if schema_table.find('.') == -1:
					iSchema ='public'
					iTable = schema_table
				if	schema_table.find('.') != -1:
					iSchema,iTable = schema_table.split('.')
				#stocker informations client dans la base
				sql ="""INSERT INTO """ + tbl_sig + """ VALUES('""" + txt_login +"""','""" + daty + """', '""" + ora + """', '""" + Nom_base + """', '""" + iSchema + """', '"""+ iTable + """', '""" + son_ip +"""','"""+ mon_ordi + """', '""" + q_version + """', 'non_spatial')"""
				cur = con.cursor()
				cur.execute(sql)
				con.commit()
				cur.close()
				#charger la couche
				uri.setConnection(sig_host,sig_port, Nom_base, role_cnx ,mdp_cnx, QgsDataSourceURI.SSLdisable)
				uri.setDataSource(iSchema,iTable,geom_column)
				uri.setKeyColumn('')
				#uri.setSrid("4326")
				vlayer = QgsVectorLayer(uri.uri(),iTable,"postgres")
				QgsMapLayerRegistry.instance().addMapLayer(vlayer)
				#Fermer base					
				con.close()

		except:
			pass
		
	
			
		
	
		