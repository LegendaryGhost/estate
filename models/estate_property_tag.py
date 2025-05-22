from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property tag\'s name must be unique')
    ]

    name = fields.Char(required=True)