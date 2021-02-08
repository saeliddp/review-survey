from v1.models import *

def clear_ratings():
    for p in Product.objects.all():
        p.num_responses = 0
        p.save()
    
    for r in Rating.objects.all():
        r.delete()

def clear_respondents():
    for r in Respondent.objects.all():
        r.delete()
        
def update_products():
    for p in Product.objects.all():
        p.num_responses = len(Rating.objects.filter(product=p))
        p.save()