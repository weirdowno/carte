from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    matriculepf = fields.Char(string='Matricule professionnel', default='0000')
    qr_link= fields.Char(string='Lien bluekango')
    blood_group = fields.Selection([ ('GS', 'GS'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Groupe sanguin', default='GS')

    

    employee_type = fields.Selection([
        ('employee', 'Employé'),
        ('apprentice', 'Apprenti')
    ], string='Type d’employé', default='employee')

    apprentice_start_date = fields.Date(string="Date d'entrée (Apprenti)")
    apprentice_end_date = fields.Date(string="Date de sortie (Apprenti)")
