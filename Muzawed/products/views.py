# views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Product
from django.http import Http404, HttpRequest,HttpResponse

def add_product_view(request):
    if request.method == 'POST':
        # Extract data from request
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        min_stock_alert = request.POST.get('min_stock_alert', 0)
        min_order_quantity = request.POST.get('min_order_quantity', 1)
        unit = request.POST.get('unit')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        # Handle the image upload
        image = request.FILES.get('image')

        # Create a new Product instance
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image,
            min_stock_alert=min_stock_alert,
            min_order_quantity=min_order_quantity,
            unit=unit,
            category=category,
            subcategory=subcategory,
        )

        # Save the product to the database
        product.save()

        # Show success message
        messages.success(request, 'Product added successfully!')

        # Redirect to a new page (e.g., product list or success page)
        return redirect("products:stock_view")

    # Prepare the context for rendering the form
    unit =Product.Unit.choices
    categories = Product.ProductCategory.choices  # Get category choices
      # Prepare subcategory choices
    subcategories = {
        'agricultural': Product.AgriculturalSubcategory.choices,
        'processed': Product.ProcessedFoodSubcategory.choices,
        'industrial': Product.IndustrialSubcategory.choices,
        'special':Product.SpecialProductsSubcategory.choices,
        'miscellaneous': Product.MiscellaneousSubcategory.choices,
    }
    return render(request, 'products/new_product.html', {'categories': categories,"unit":unit ,"subcategories":subcategories})

def remove_product_view(request:HttpRequest , product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return redirect("products:stock_view")
    except Http404 as e:
        return redirect('main:index_view')
    except Exception as error:
        return redirect('main:index_view')


def update_product_view(request: HttpRequest, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            product.name = request.POST.get('name')
            product.description = request.POST.get('description', '')
            product.price = request.POST.get('price')
            product.stock = request.POST.get('stock')
            product.min_stock_alert = request.POST.get('min_stock_alert', 0)
            product.min_order_quantity = request.POST.get('min_order_quantity', 1)
            product.unit = request.POST.get('unit')
            product.category = request.POST.get('category')
            product.subcategory = request.POST.get('subcategory')

            # Debugging output
            print("------------------------------------")
            print(f"Category: {request.POST.get('category')}")
            print(f"Subcategory: {request.POST.get('subcategory')}")

            # Handle the image upload
            if "image" in request.FILES:
                product.image = request.FILES["image"]

            # Save the product to the database
            product.save()
            return redirect("products:stock_view")

        else:
            unit = Product.Unit.choices
            categories = Product.ProductCategory.choices  # Get category choices
            subcategories = {
                'agricultural': Product.AgriculturalSubcategory.choices,
                'processed': Product.ProcessedFoodSubcategory.choices,
                'industrial': Product.IndustrialSubcategory.choices,
                'special': Product.SpecialProductsSubcategory.choices,
                'miscellaneous': Product.MiscellaneousSubcategory.choices,
            }

            return render(request, "products/update_product.html", {
                "product": product,
                "categories": categories,
                "unit": unit,
                "subcategories": subcategories
            })

    except Http404 as e:
        print(e)
        return redirect('main:index_view')
    except Exception as error:
        print(error)
        return redirect('main:index_view')
    
def stock_view(request:HttpRequest):
    products = Product.objects.all()
    print(products[0].subcategory)
    # return render(request, 'product_list.html', {'products': products})

    return render(request, "products/product_stock.html",{'products': products})