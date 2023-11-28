import pyodbc 
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError



class connector(models.Model):

    _name = "connector"

    name = fields.Char()

    def connect(self): 
        conn_str = f'FILEDSN=C://Users/amal.abdelmajid/Desktop/[ODBC].dsn'
        cnxn = pyodbc.connect("DSN=KEYLOOP1")
        raise UserError(str(cnxn))
        cursor = cnxn.cursor()
        cursor.execute("select * from DD_01_PRICE")
        row = cursor.fetchall()
        # self.write(row)
        raise UserError(str(row))