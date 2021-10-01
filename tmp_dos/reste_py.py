if self.mon_UI.liste_table.count()>0:
			try:
				isany = 0
				itemsList = self.mon_UI.liste_table.selectedItems()
				for item_Isa in itemsList:
					isany += 1
				
				if isany > 0:
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
					uri = QgsDataSourceURI()
					if val_base_encours=='spatial': 
						con = None
						con = psycopg2.connect("dbname='" + bd_charger + "' user='" + role_carte+ "' password='" + mdp_carte + "' host='" + sig_host + "' port='"+ sig_port +"'")
						for item in itemsList:
							iSchema,iTable = item.text().split('.')
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
							#fermer cnx_carte
						
						#Fermer base					
						con.close()
							
					
					if val_base_encours=='non_spatial': 
						#geom_column = ''
						geom_column = None
						con = None
						con = psycopg2.connect("dbname='" + bd_charger + "' user='" + role_carte + "' password='" + mdp_carte + "' host='" + sig_host + "' port='"+ sig_port +"'")
						for item in itemsList:
							if item.text().find('.') == -1:
								iSchema ='public'
								iTable = item.text()
							if	item.text().find('.') != -1:
								iSchema,iTable = item.text().split('.')
								
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
			