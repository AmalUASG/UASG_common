import pyodbc 

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError



class connector(models.Model):


	_name = "connector"



	name = fields.Char()

	def connect(self): 

		cnxn = pyodbc.connect(host='10.200.209.225', database='RemsDB',port=1433)

		raise UserError(str(cnxn ))
