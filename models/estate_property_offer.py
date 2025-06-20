from odoo import api, fields, models, exceptions, tools

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    _sql_constraints = [
        ('positive_price', 'CHECK(price > 0)', 'The offer\'s price must be strictly positive')
    ]
    _order = "price DESC"

    price = fields.Float()
    state = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    validity = fields.Integer(default=7, string="Validity (days)")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days
            else:
                offer.validity = 0

    def accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise exceptions.UserError("The property '%s' has already been sold" % offer.property_id.name)
            offer.state = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
        return True

    def refuse(self):
        for offer in self:
            offer.state = "refused"
        return True
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            property.state = 'offer_received'
            max_offer_price = max(property.offer_ids.mapped('price'), default=0.0)
            if tools.float_compare(vals['price'], max_offer_price, precision_digits=2) == -1:
                raise exceptions.UserError("The offer price must be at least %d" % max_offer_price)
        return super(EstatePropertyOffer, self).create(vals_list)