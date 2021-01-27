from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from v1.models import *
from random import randint, shuffle

def entry(request):
    # create new Respondent in database
    respondent = Respondent()
    products = Product.objects.filter(num_responses__lt=5)
    indices = [i for i in range(len(products))]
    
    selected_prod = products[indices.pop(randint(0, len(indices) - 1))]
    p_seq = str(selected_prod.id)
    selected_prod.num_responses += 1
    selected_prod.save()
    for _ in range(14):
        selected_prod = products[indices.pop(randint(0, len(indices) - 1))]
        p_seq += " " + str(selected_prod.id)
        selected_prod.num_responses += 1
        selected_prod.save()
        
    respondent.product_seq = p_seq
    respondent.save()
    return redirect("driver", respondent.id, respondent.position)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def driver(request, respondent_id, position):
    # find user, compare given position with database position
    respondent = Respondent.objects.get(id=respondent_id)
    
    if respondent.position == position: # normal case
        if respondent.position == 0:
            if "instr_submit" in request.GET:
                # increment position in database
                respondent.position += 1
                respondent.save()
                return redirect("survey", respondent_id, respondent.position)
            else:
                return redirect("instructions", respondent_id, respondent.position)
        else:
            # update db with responses
            if "surv_submit" in request.GET:
                rev1radio = "radio" + str(request.GET["review1place"])
                rev2radio = "radio" + str(request.GET["review2place"])
                rev3radio = "radio" + str(request.GET["review3place"])
                
                prod_id = int(respondent.product_seq.split(" ")[0])
                prod = Product.objects.get(id=prod_id)
                
                Rating(respondent=respondent, product=prod, 
                        review1_rating=request.GET[rev1radio],
                        review2_rating=request.GET[rev2radio],
                        review3_rating=request.GET[rev3radio]).save()
                
                respondent.position += 1
                if " " in respondent.product_seq:
                    respondent.product_seq = respondent.product_seq[respondent.product_seq.index(" ") + 1:]
                else:
                    #redirect to thank you page
                    respondent.product_seq = "Done"
                    respondent.save()
                    return redirect("thanks", respondent_id)
                respondent.save()
            return redirect("survey", respondent_id, respondent.position)
    else: # trying to use back button case
        return redirect("driver", respondent_id, respondent.position)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)       
def instructions(request, respondent_id, position):
    respondent = Respondent.objects.get(id=respondent_id)
    if respondent.position != position:
        return redirect("driver", respondent_id, respondent.position)

    context = {
        "respondent_id": respondent_id,
        "position": position
    }
    return render(request, "v1/instructions.html", context)

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

def thanks(request, respondent_id):
    context = {
        'respondent_id': respondent_id
    }
    if 'mturk_id' in request.GET:
        resp = Respondent.objects.get(id=respondent_id)
        resp.mturk_id = request.GET['mturk_id'][:50]
        resp.save()
        return render(request, 'v1/code.html')
    else:
        return render(request, 'v1/thanks.html', context)