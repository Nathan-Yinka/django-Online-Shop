from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from cart.form import CartAddProductForm

# Create your views here.
def product_list(request,category_slug=None):
    category = None
    products =  Product.objects.filter(available=True)
    categories = Category.objects.all()
    print(categories)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
        
    context = {
        'category': category,
        "products":products,
        "categories":categories,
    }
    return render(request, 'shop/product/list.html',context)

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available = True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',{'product': product,"cart_product_form":cart_product_form})
    