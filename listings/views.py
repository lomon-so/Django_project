from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import bedroom_choices, price_choices, state_choices 

# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    
    paginator = Paginator(listings, 3)  # Show 3 contacts per page.

    page_number = request.GET.get('page')
    page_listings = paginator.get_page(page_number)
    
    context = {
        'listings' : page_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    context = {
        'listing' : listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date') #[:3]
    
    # Search Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
            
    # Search city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
            
            
    # Search State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
            
    # Search Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms=int(bedrooms))
            
    # Search Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price=int(price)) # [(price__lte=int(price))=anything priced at or below]
    
    context = {
        'bedroom_choices' : bedroom_choices,
        'price_choices' : price_choices, 
        'state_choices' : state_choices, 
        'listings' : queryset_list, 
        'values' : request.GET 
    }
    return render(request, 'listings/search.html', context )