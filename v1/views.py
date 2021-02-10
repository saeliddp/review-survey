from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from v1.models import *
from random import randint, shuffle
import csv, datetime

responses_per_prod = 3
responses_per_user = 3

# prod_seq_entries should be a list of product ids
def get_next_product(prod_seq_entries=[]):
    global responses_per_prod
    
    products = Product.objects.filter(num_responses__lt=responses_per_prod)
    # FOR TESTING ONLY
    products = products.filter(id__lt=4)
    #print(len(products))
    indices = []
    prod_seq_entries = [int(i) for i in prod_seq_entries]
    
    for i, p in enumerate(products):
        if p.id not in prod_seq_entries:
            indices.append(i)
    
    if len(indices) == 0:
        return None
    else:
        product = products[indices[randint(0, len(indices) - 1)]]
        product.num_responses += 1
        product.save()
        return product
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)       
def instructions(request):
    global responses_per_prod
    global responses_per_user
    if "instr_submit" in request.GET:
        #user pressed begin, must create user        
        respondent = Respondent()
        respondent.save()
        return redirect("driver", respondent.id, respondent.position)
    else:
        return render(request, "v1/instructions.html")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def driver(request, respondent_id, position):
    global responses_per_prod
    global responses_per_user
    # find user, compare given position with database position
    respondent = Respondent.objects.get(id=respondent_id)
    
    if respondent.position == position: # normal case 
        prod_seq_entries = respondent.product_seq.split(" ")
        respondent.position += 1
        
        if prod_seq_entries[0] == "None": # first survey
            next_prod = get_next_product()
            if next_prod is None:
                return render(request, "v1/complete.html")
            else:
                respondent.product_seq = str(next_prod.id)
                respondent.save()
                return redirect("survey", respondent_id, respondent.position)
                
        elif prod_seq_entries[0] == "Factors":
            if "factors" in request.GET:
                respondent.product_seq = "MTurk " + respondent.product_seq
                respondent.factors = request.GET["factors"][:255]
                if "additional" in request.GET:
                    respondent.additional = request.GET["additional"][:255]
                respondent.save()
                return redirect("thanks", respondent_id, respondent.position)
            respondent.save()
            return redirect("thoughts", respondent_id, respondent.position)
        
        elif prod_seq_entries[0] == "MTurk":
            if "mturk_id" in request.GET:
                respondent.mturk_id = request.GET["mturk_id"][:50]
                respondent.save()
                return render(request, "v1/code.html")
            respondent.save()
            return redirect("thanks", respondent_id, respondent.position)
            
        elif len(prod_seq_entries) <= responses_per_user:
            if "surv_submit" in request.GET:
                rev1radio = "radio" + str(request.GET["review1place"])
                rev2radio = "radio" + str(request.GET["review2place"])
                rev3radio = "radio" + str(request.GET["review3place"])
                
                prod_id = int(respondent.product_seq.split(" ")[0])
                prod = Product.objects.get(id=prod_id)
                
                Rating(respondent=respondent, product=prod, 
                        review1_rating=request.GET[rev1radio],
                        review2_rating=request.GET[rev2radio],
                        review3_rating=request.GET[rev3radio],
                        time_elapsed=request.GET["time_elapsed"]).save()
                if len(prod_seq_entries) < responses_per_user:
                    next_prod = get_next_product(respondent.product_seq.split(" "))
                    if next_prod is None:
                        respondent.product_seq = "Factors " + respondent.product_seq
                        respondent.save()
                        return redirect("driver", respondent_id, respondent.position)
                    else:
                    
                        respondent.product_seq = str(next_prod.id) + " " + respondent.product_seq
                        respondent.save()
                        return redirect("survey", respondent_id, respondent.position)
                else:
                    respondent.product_seq = "Factors " + respondent.product_seq
                    respondent.save()
                    return redirect("driver", respondent_id, respondent.position)
            else:
                respondent.position -= 1
                respondent.save()
                return redirect("survey", respondent_id, respondent.position)
            
    else:
        return redirect("driver", respondent_id, respondent.position)
       

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def survey(request, respondent_id, position):
    respondent = Respondent.objects.get(id=respondent_id)
    if respondent.position != position:
        return redirect("driver", respondent_id, respondent.position)
    prod_id = int(respondent.product_seq.split(" ")[0])
    product = Product.objects.get(id=prod_id)
    
    review_arrangement = [product.review1, product.review2, product.review3]
    shuffle(review_arrangement)
    context = {
        "name": product.name,
        "description": product.description,
        "review1": review_arrangement[0],
        "review1place": review_arrangement.index(product.review1) + 1,
        "review2": review_arrangement[1],
        "review2place": review_arrangement.index(product.review2) + 1,
        "review3": review_arrangement[2],
        "review3place": review_arrangement.index(product.review3) + 1,
        "respondent_id": respondent_id,
        "position": position
    }
    return render(request, "v1/survey.html", context)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def thoughts(request, respondent_id, position):
    respondent = Respondent.objects.get(id=respondent_id)
    if respondent.position != position:
        return redirect("driver", respondent_id, respondent.position)
    context = {
        'respondent_id': respondent_id,
        'position': position
    }
    return render(request, 'v1/thoughts.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def thanks(request, respondent_id, position):
    respondent = Respondent.objects.get(id=respondent_id)
    if respondent.position != position:
        return redirect("driver", respondent_id, respondent.position)
    context = {
        'respondent_id': respondent_id,
        'position': position
    }
    return render(request, 'v1/thanks.html', context)

def export_users(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['id', 'mturk_id', 'pages_completed', 'factors', 'additional', 'date'])
    
    for u in Respondent.objects.all().values_list('id', 'mturk_id', 'position', 'factors', 'additional', 'date'):
        writer.writerow(u)
    
    today = datetime.date.today()
    filename = "users_" + today.strftime("%m_%d_%Y") + ".csv"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response

def export_ratings(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['user_id', 'product_id', 'product_amazon_id', 'review1_rating', 'review2_rating', 'review3_rating', 'time_elapsed'])
    
    for r in Rating.objects.all():
        writer.writerow([r.respondent.id, r.product.id, r.product.amazon_id, r.review1_rating, r.review2_rating, r.review3_rating, r.time_elapsed])
    
    today = datetime.date.today()
    filename = "ratings_" + today.strftime("%m_%d_%Y") + ".csv"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response

def export_products(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'amazon_id', 'review1', 'review2', 'review3', 'num_responses'])
    
    for p in Product.objects.all():
        writer.writerow([p.id, p.name, p.amazon_id, p.review1, p.review2, p.review3, p.num_responses])
        
    today = datetime.date.today()
    filename = "products_" + today.strftime("%m_%d_%Y") + ".csv"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response