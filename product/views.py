from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .models import *
from custom_user.models import *
from django.views import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q






class IndexView(View):
    def get(self, request):
        carousel = Advertise.objects.filter(status=True)
        categories = Category.objects.filter(status=True)
        category_posts_data = {}
        search = request.GET.get("search","")
        for category in categories:
            if search:
                products = Product.objects.filter(category=category).filter(Q(name__icontains=search) | Q(description__icontains=search))
            else:
                products = Product.objects.filter(category=category)[:4]

            products_data = []
            for product in products:
                original_price = product.price - (product.discount) if product.discount else product.price
                products_data.append({
                    'product': product,
                    'original_price': original_price,
                })

            category_posts_data[category] = products_data
        return render(request, 'index.html', {'categories':category_posts_data, 'carousel':carousel})
    

def DetailView(request,id):
    product = Product.objects.get(id=id)
    comment = Review.objects.filter(product = id)
    original_price = product.price - (product.discount) if product.discount else product.price

    low_stock_message = None
    if product.stock < 5:
        low_stock_message = f" {product.stock} items only Left!"
    context = {
        'low':low_stock_message,
        'product': product,
        'price': original_price,
        'comments' : comment
    }

    return render(request,'details.html',context)

@login_required(login_url='login')
def AddOrder(request, id):
    prod = get_object_or_404(Product, id=id)

    if prod.stock < 1:
        return redirect('details', id=id)  
    
    order, created = Order.objects.get_or_create(user=request.user)
    discounted_price = prod.price - (prod.discount if prod.discount else 0)
    
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=prod,
        defaults={'quantity': 1, 'price': discounted_price})

    if not created:
        order_item.quantity += 1
        order_item.save()

    prod.stock -= 1
    prod.save()

    return redirect('cartview')

@login_required(login_url='login')
def OrderView(request):
    order = get_object_or_404(Order, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    for item in order_items:
        item.discounted_price = item.price
        item.total_price = item.discounted_price * item.quantity

    total_price = sum(item.total_price for item in order_items)

    return render(request, 'cart/cart2.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    })

    
class Remove_Order(View):
    def get(self, request,order_id):
        cart_item = get_object_or_404(OrderItem, id=order_id)
        cart_item.product.stock += cart_item.quantity
        cart_item.product.save()
        cart_item.delete()
        return redirect('cartview')


@csrf_protect
def increase_quantity(request, order_id):
    cart_item = get_object_or_404(OrderItem, id=order_id)
    if cart_item.product.stock < 1:
        messages.error(request, 'This item is out of stock.')
        return redirect('cartview')
    
    cart_item.quantity += 1
    cart_item.save()
    # Decrease the product stock
    cart_item.product.stock -= 1
    cart_item.product.save()  # Save the product instance
    messages.success(request, 'Item quantity increased.')
    return redirect('cartview')




@csrf_protect
def decrease_quantity(request, order_id):
    cart_item = get_object_or_404(OrderItem, id=order_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        cart_item.product.stock += 1
        cart_item.product.save() 
        messages.success(request, 'Item quantity Decrease.')
    else:
        cart_item.delete()
    return redirect('cartview')
 
class PaymentView(View):
    def get(self, request):
        addr = ShippingAddress.objects.filter(user = request.user)
        return render(request, 'cart/payment.html', {'addr':addr})
    
    def post(self, request):
        selected_items_ids = request.POST.getlist('selected_items')
        address = request.POST.get('adr')
        selected_items_ids_int = []
        for id in selected_items_ids:
            selected_items_ids_int.append(int(id))
        selected_items = OrderItem.objects.filter(id__in=selected_items_ids_int)

        for item in selected_items:
            item.discounted_price = item.price
            item.total_price = item.discounted_price * item.quantity

        total_price = sum(item.total_price for item in selected_items)
        total_price = sum(item.price * item.quantity for item in selected_items)  

        return render(request, 'cart/payment.html', {
            'selected_items': selected_items,
            'total_price': total_price,
        })


class CategoryBasedView(View):
    def get(self, request, id):
        cate = Category.objects.get(id = id)
        post = Product.objects.filter(category = cate)
        return render (request, 'categorybased.html',{'cate':cate, 'post':post})


class ReviewView(View):
   
    def post(self, request, id):
        prod = get_object_or_404(Product, id=id)
        comment = request.POST.get('message')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')

        review = Review(user=request.user, product=prod, comment=comment, rating=rating, image=image)
        review.save()
        
        return redirect('details' ,id=id)

# def OrderView(request):
#     order = get_object_or_404(Order, user=request.user)
#     order_item = OrderItem.objects.all()
#     for item in order_item:
#         item.total_price = item.price * item.quantity
#     total_price = sum(item.total_price for item in order_item)
#     return render(request, 'cart/cart2.html', {'order': order, 'order_items': order_item,'total_price':total_price})


# class increase_quantity(View):
#     def post(self, request,order_id):
#         cart_item = get_object_or_404(OrderItem, id=order_id)
#         if cart_item.product.stock < 1:
#             messages.error(request, 'This item is out of stock.')
#             return redirect('cartview')
        
#         cart_item.quantity += 1
#         cart_item.save()
#         # Decrease the product stock
#         cart_item.product.stock -= 1
#         cart_item.product.save()  # Save the product instance
#         messages.success(request, 'Item quantity increased.')
#         return redirect('cartview')

# class decrease_quantity(View):
#     def get(self, request, order_id):
#         cart_item = get_object_or_404(OrderItem, id=order_id)
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#             cart_item.product.stock += 1
#             cart_item.product.save() 
#             messages.success(request, 'Item quantity Decrease.')
#         else:
#             cart_item.delete()
#         return redirect('cartview')


# class IndexView(View):
#     def get(self, request):
#         categories = Category.objects.prefetch_related('products').filter(status=True)

#         return render(request, 'index.html', {'categories':categories})