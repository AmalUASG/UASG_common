import pyodbc 

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError



class connector(models.Model):


	_name = "connector"



	name = fields.Char()

	def connect(self): 

		cnxn = pyodbc.connect('driver=MySQL', host='localhost', database='RemsDB')

		raise UserError(str(cnxn ))
