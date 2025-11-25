from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO
from odoo.modules.module import get_module_resource

class HrProfessionalCard(models.Model):
    _name = 'hr.professional.card'
    _description = 'Carte professionnelle'

    name = fields.Char(string='Numéro de carte', required=True, copy=False, readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employé', required=True)
    matriculepf = fields.Char(string='Matricule professionnel', related='employee_id.matriculepf', store=True)
    profession = fields.Char(string='Profession / Poste', related='employee_id.job_title', store=True)
    blood_group = fields.Selection(related='employee_id.blood_group', string='Groupe sanguin', store=True)
    issue_date = fields.Date(string='Date de délivrance', default=fields.Date.today)
    apprentice_start_date = fields.Date(string="Date d'entrée", related='employee_id.apprentice_start_date', store=True)
    apprentice_end_date = fields.Date(string="Date de sortie", related='employee_id.apprentice_end_date', store=True)
    
    employee_type = fields.Selection(
        related='employee_id.employee_type',
        string="Type d'employé",
        store=True
    )
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('issued', 'Délivrée'),
        ('returned', 'Restituée')
    ], string='État', default='draft')
    

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.professional.card') or 'New'
        return super().create(vals)

    
    
    def print_card(self):
     return self.env.ref('carte.action_report_hr_professional_card').report_action(self)            
    
    def print_release(self):
        """Imprimer la décharge de remise de badge"""
        return self.env.ref('carte.action_report_hr_professional_card_release').report_action(self)
    
    def _generate_qr_code(self):
        """Génère le QR code à partir du lien saisi"""
        for card in self:
            if card.qr_link:
                try:
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(card.qr_link)
                    qr.make(fit=True)
                    
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")
                    card.qr_code = base64.b64encode(buffer.getvalue())
                except Exception as e:
                    card.qr_code = False
            else:
                card.qr_code = False
    
    # Champs
    qr_link = fields.Char(string="Lien pour QR Code", help="Saisissez le lien à encoder dans le QR code")
    qr_code = fields.Binary(string="QR Code", compute='_compute_qr_code', store=True)
    
    @api.depends('qr_link')
    def _compute_qr_code(self):
        """Compute field pour générer le QR code"""
        self._generate_qr_code()


    @api.model
    def get_company_logo(self):
        """Retourne le logo CITA en base64"""
        img_path = get_module_resource('carte', 'static', 'src', 'img', 'cital.png')
        if img_path:
            try:
                with open(img_path, 'rb') as f:
                    return base64.b64encode(f.read())
            except Exception as e:
                return False
        return False 
    