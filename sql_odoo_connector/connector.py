import pyodbc 
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError



class connector(models.Model):

	_name = "connector"

	name = fields.Char()

	def connect(self): 


		raise UserError(str(pyodbc.connect('Driver={ODBC Driver 17 for SQL Server},Server=localhost,DATABASE=RemsDB,LongAsMax=yes,Trusted_Connection=yes')
))

		print (cnxn)