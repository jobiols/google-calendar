# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------
import odoorpc
import google_event
from secret import PASSWORD

DESDE = '2017-08-15'
HASTA = '2017-12-30'

login = {
    'server': '18.220.25.10',
    'port': 8068,
    'database': 'makeover_datos',
    'username': 'admin',
    'password': PASSWORD,
}

# conectar con odoo, proveer credenciales
odoo = odoorpc.ODOO(login.get('server'), port=login.get('port'))
odoo.login(login.get('database'), login.get('username'), login.get('password'))
print 'conectado con odoo'

# conectar con google, proveer credenciales
google = google_event.google()
google.connect()
print 'conectado con google'

# obtener objeto lecture de odoo server
lecture_obj = odoo.env['curso.lecture']
ids = lecture_obj.search([('date', '>', DESDE),('date', '<', HASTA)])
print 'ya tengo todas las lectures'

# limpiar el calendario de google
google.clear()
print 'ya borre el calendario de google'

# volver a cargar todos los eventos
for lecture in lecture_obj.browse(ids):
    ge = google_event.google_event(lecture)
    google.insert(ge)
