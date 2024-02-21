from django.shortcuts import render,redirect
from .models import Order,OrderItem
from .form import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm (data=request.POST)
        if form.is_valid() and cart.__len__()>0:
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item["price"],
                    quantity=item["quantity"]
                )
            cart.clear()
            
            # launch asynchronous task
            order_created.delay(order.id)
            
            # set the order id in the sesssion
            request.session['order_id'] = order.id
            
            return redirect("payment:process")
        else :
            return redirect("cart:cart_detail")
    else:
        form = OrderCreateForm ()
        return render(request, "orders/order/create.html",{"form":form})
