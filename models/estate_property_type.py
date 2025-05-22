from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property type\'s name must be unique')
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id",string="Properties")