
from django.utils.translation import gettext_lazy as _
from django.db import models

class CATEGORIES(models.TextChoices):
    GCD = 'GCD', _('General Car Discussion')
    CA ='CA', _('Car Accessories')
    CP = 'CP', _('Car Performance Parts')
    CC = 'CC', _('Continental Cars')
    CEI = 'CEI', _('Cosmetic Enhancement Items')
    ICE = 'ICE', _('In Car Entertainment')
    JC = 'JC', _('Japanese Cars')
    MR = 'MR', _('Maintenance & Repairs')
    TR = 'TR', _('Tyres & Rims')
    OTHER = 'O', _('NON CAR-RELATED')
    
def get_category_display(category):
    if category == 'GCD':
        return  _('General Car Discussion')
    elif category == 'CA':
        return  _('Car Accessories')
    elif category ==  'CP':
        return  _('Car Performance Parts')
    elif category ==  'CC':
        return  _('Continental Cars')
    elif category ==  'CEI':
        return  _('Cosmetic Enhancement Items')
    elif category ==  'ICE':
        return  _('In Car Entertainment')
    elif category ==  'JC':
        return  _('Japanese Cars')
    elif category ==  'MR':
        return  _('Maintenance & Repairs')
    elif category ==  'TR':
        return  _('Tyres & Rims')
    else:
        return  _('NON CAR-RELATED')
    
    
def get_all_categories_and_displays():
    return [
            {
                "category" : 'GCD',
                "category_display":    _('General Car Discussion')
            },
            
            {
                "category" : 'CA',
                "category_display":    _('Car Accessories')
            },
            
            {
                "category" : 'CP',
                "category_display":    _('Car Performance Parts')
            },
            
           {
                "category" : 'CC',
                "category_display":    _('Continental Cars')
            },
            
            {
                "category" : 'CEI',
                "category_display":    _('Cosmetic Enhancement Items')
            },
            
            {
                "category" : 'ICE',
                "category_display":    _('In Car Entertainment')
            },
            
            {
                "category" : 'JC',
                "category_display":    _('Japanese Cars')
            },
            
           {
                "category" : 'MR',
                "category_display":    _('Maintenance & Repairs')
            },
            
            {
                "category" : 'TR',
                "category_display":    _('Tyres & Rims')
            },
            
            {
                "category" : 'O',
                "category_display":    _('NON CAR-RELATED')
            },
            
            
            ]