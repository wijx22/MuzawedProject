# views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages

from accounts.models import SupplierProfile
from supplier.models import City
from .models import Product
from django.http import Http404, HttpRequest,HttpResponse
from notification.models import Notification

                       
def add_product_view(request):
    if request.user.is_authenticated:
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
            city_id = request.POST.get('city')  
            print(city_id)

            # Handle the image upload
            image = request.FILES.get('image')

            # Create a new Product instance
            product:Product = Product(
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

            if city_id:
                product.City = City.objects.get(id=city_id) 
            # Save the product to the database
            product.save()
            # Notification.objects.create(
            #                         recipient=request.user,
            #                         notification_type='alert',
            #                         message=f'تم إضافة المنتج "{product.name}" إلى متجرك.'
            #                     )

            # Show success message
            messages.success(request, 'تم إضافة المنتج بنجاح')

            # Redirect to a new page (e.g., product list or success page)
            return redirect("products:stock_view")


        try:
            # Check if the user is a supplier
            supplier:SupplierProfile = request.user.supplier
            covered_cities = supplier.cities_covered.all()  
           
  
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
        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة عرض المعلومات ')
            return redirect("main:index_view")

 
    return render(request, 'products/new_product.html', 
                  {'categories': categories,
                   "unit":unit ,
                   "subcategories":subcategories,"covered_cities":covered_cities})

def remove_product_view(request:HttpRequest , product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        Notification.objects.create(
                                 recipient=request.user,
                                 notification_type='alert',
                                 message=f'تم حذف المنتج "{product.name}" من قائمتك.'
                             )

        return redirect("products:stock_view")
    except Http404 as e:
        print("an erro",e)
        return redirect('main:index_view')
    except Exception as error:
        print("an erro",error)

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

            if "image" in request.FILES:
                product.image = request.FILES["image"]

            # Save the product to the database
            product.save()
            Notification.objects.create(
                                    recipient=request.user,
                                    notification_type='alert',
                                    message=f'تم تعديل تفاصيل المنتج "{product.name}" بنجاح.'
                                )
            return redirect("products:stock_view")

        else:
            unit = Product.Unit.choices
            categories = Product.ProductCategory.choices 
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
     if request.user.is_authenticated:
        try:
            supplier: SupplierProfile = request.user.supplier
            covered_cities = supplier.cities_covered.all()  # Get cities covered by the supplier

            # Get the city_id from the query parameters
            city_id = request.GET.get('city_id')

            # Filter products based on the selected city
            if city_id:
                # Filter products for the current supplier that are in the selected city
                products = Product.objects.filter(City__id=city_id, City__suppliers=supplier)
            else:
                # If no city is selected, return all products for cities covered by the supplier
                products = Product.objects.filter(City__suppliers=supplier)

           

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة عرض المعلومات ')
            return redirect("main:index_view")




        return render(request, "products/product_stock.html",{'products': products ,"covered_cities":covered_cities})

def product_details_view(request:HttpRequest,product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)


       
        return render(request,"products/product_details.html",{"product": product})
    except Http404 as e:
        print(e)
        return redirect('main:index_view')
    except Exception as error:
        print(error)
        return redirect('main:index_view')
    

def products_view(request:HttpRequest):
    products = Product.objects.all()

    return render(request, "products/product_list.html",{'products': products})
        
