from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepeted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default=('new')
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")