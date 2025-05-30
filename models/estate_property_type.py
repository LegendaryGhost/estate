from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property type\'s name must be unique')
    ]
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)