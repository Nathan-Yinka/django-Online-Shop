from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from cart.form import CartAddProductForm
from shop.recommeder import Recommender

# Create your views here.
def product_list(request,category_slug=None):
    category = None
    products =  Product.objects.filter(available=True)
    categories = Category.objects.all()
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,translations__language_code=language,translations__slug=category_slug)
        products = products.filter(category=category)
        
    
        
    context = {
        'category': category,
        "products":products,
        "categories":categories,
    }
    return render(request, 'shop/product/list.html',context)

def product_detail(request,id,slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,id=id,translations__slug=slug,translations__language_code=language,available = True)
    r = Recommender()
    recommended_products = r.suggest_products_for([product],4)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',{'product': product,"cart_product_form":cart_product_form,"recommended_products":recommended_products})
    