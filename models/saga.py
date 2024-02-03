# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api

class LibroSaga(models.Model):
    _name = 'sagas.saga'
    _description = 'Sagas'
    _order = 'nombre'
    _rec_name = 'nombre'

    nombre = fields.Char('Titulo', required=True, index=True)
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)
    fecha_publicacion = fields.Date('Fecha publicación')
    autor_ids = fields.Many2many('libro.autor')
    libro_ids = fields.Many2many('ligros.libro')
    n_libros = 0
