{
    'name': 'Gestion des cartes professionnelles',
    'version': '16.0.1.0',
    'summary': 'Gestion et impression des cartes professionnelles avec QR code',
    'category': 'Human Resources',
    'author': 'TonNom',
    'depends': ['base', 'hr'],
    'data': [
        
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_professional_card_views.xml',
        'reports/hr_professional_card_report.xml',
    ],
    'installable': True,
    'application': True,
}
