# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def add_product_view(request):
    if request.method == 'POST':
        # Extract data from request
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        min_stock_alert = request.POST.get('min_stock_alert', 0)
        min_order_quantity = request.POST.get('min_order_quantity', 1)
        sale_method = request.POST.get('sale_method')
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
            sale_method=sale_method,
            category=category,
            subcategory=subcategory,
        )

        # Save the product to the database
        product.save()

        # Show success message
        messages.success(request, 'Product added successfully!')

        # Redirect to a new page (e.g., product list or success page)
        return redirect('main:index_view')  # Adjust the redirect URL as needed

    # Prepare the context for rendering the form
    sale_method =Product.SaleMethodChoices.choices
    categories = Product.ProductCategory.choices  # Get category choices
      # Prepare subcategory choices
    subcategories = {
        'agricultural': Product.AgriculturalSubcategory.choices,
        'processed': Product.ProcessedFoodSubcategory.choices,
        'industrial': Product.IndustrialSubcategory.choices,
        'special':Product.SpecialProductsSubcategory.choices,
        'miscellaneous': Product.MiscellaneousSubcategory.choices,
    }
    print(subcategories)
    return render(request, 'products/new_product.html', {'categories': categories,"sale_method":sale_method ,"subcategories":subcategories})