# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Fichero abstracto'

    activo = fields.Boolean(default=True)

    def archivar(self):
        for record in self:
            record.activo = not record.activo

class LibroSaga(models.Model):
    _name = 'libro.saga'
    _inherit = ['base.archive']
    _description = 'Sagas'
    _order = 'fecha_publicacion desc, nombre'

    _rec_name = 'nombre'

    nombre = fields.Char('Titulo', required=True, index=True)
    
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)

    portada = fields.Binary('Portada Saga')

    # Fecha de publicación
    fecha_publicacion = fields.Date('Fecha publicación')

    autor_ids = fields.Many2many('libro.autor')

    #Relacion muchos a uno con el modelo de las categorias
    libro_ids = fields.Many2many('libro')
    
    #Variable computada para calcular dias desde el lanzamiento
    dias_lanzamiento = fields.Integer(
        string='Dias desde lanzamiento',
        compute='_compute_anyo', inverse='_inverse_anyo', search='_search_anyo',
        store=False,
        compute_sudo=True,
    )

    #Funcion usada para obtener que modelos pueden ser referenciados 
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.depends('fecha_publicacion')
    def _compute_anyo(self):
        hoy = fields.Date.today()
        for saga in self:
            if saga.fecha_publicacion:
                delta = hoy - saga.fecha_publicacion
                saga.dias_lanzamiento = delta.days
            else:
                saga.dias_lanzamiento = 0


    def _inverse_anyo(self):
        hoy = fields.Date.today()
        for saga in self.filtered('fecha_publicacion'):
            d = hoy - timedelta(days=saga.dias_lanzamiento)
            saga.fecha_publicacion = d

    def _search_age(self, operator, value):
        hoy = fields.Date.today()
        value_dias = timedelta(dias=value)
        value_fecha = hoy - value_dias
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('fecha_publicacion', new_op, value_fecha)]

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.nombre, record.fecha_publicacion)
            result.append((record.id, rec_name))
        return result

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El titulo de la saga debe ser único.'),
        ('positive_libros', 'CHECK(libros>0)', 'La saga debe tener al menos un libro')
    ]

    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe ser anterior a la actual')