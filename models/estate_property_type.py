from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property type\'s name must be unique')
    ]
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many("estate.property", "property_type_id",string="Properties")