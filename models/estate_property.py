from odoo import api, fields, models, exceptions, tools

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]
    _order = "id DESC"

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
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default=('new'),
        string="Status"
    )

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def _check_price_percentage(self):
        for property in self:
            if not tools.float_is_zero(property.selling_price, precision_digits=2) and tools.float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) == -1:
                raise exceptions.ValidationError("The selling price must be atleast 90% of the expected price. Please raises the offer price or lower the excpected price to fix this.")

    def action_set_sold_state(self):
        for property in self:
            if property.state == "cancelled":
                raise exceptions.UserError("Cancelled properties cannot be sold")
            property.state = "sold"
        return True

    def action_set_cancelled_state(self):
        for property in self:
            if property.state == "sold":
                raise exceptions.UserError("Sold properties cannot be cancelled")
            property.state = "cancelled"
        return True
    
    @api.ondelete(at_uninstall=False)
    def _unlink_check_state(self):
        for property in self:
            if not property.state in ('new', 'cancelled'):
                raise exceptions.UserError("Only new and cancelled properties can be deleted")