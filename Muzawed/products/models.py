from django.db import models

# Create your models here.

from django.db import models

class Product(models.Model):
    class Unit(models.TextChoices):
        UNIT = 'unit', 'حبة'
        KG = 'kg', 'كيلو'
        CARTON = 'carton', 'كرتون'
        BOX = 'box', 'صندوق'
        LITER = 'liter', 'للتر'
        PACKET = 'packet', 'بالعبوة'
        SET = 'set', 'بالمجموعة'
        POUND = 'pound', 'بالرطل'
        BAG = 'bag', 'بالكيس'

    class ProductCategory(models.TextChoices):
        AGRICULTURAL_PRODUCTS = 'agricultural', 'المنتجات الزراعية'
        PROCESSED_FOOD = 'processed', 'المنتجات الغذائية المصنعة'
        INDUSTRIAL_PRODUCTS = 'industrial', 'المنتجات الصناعية'
        SPECIAL_PRODUCTS = 'special', 'المنتجات الخاصة'
        MISCELLANEOUS = 'miscellaneous', 'منتجات متنوعة'

    class AgriculturalSubcategory(models.TextChoices):
        GRAINS = 'grains', 'الحبوب'
        LEGUMES = 'legumes', 'البقوليات'
        VEGETABLES = 'vegetables', 'الخضروات'
        FRUITS = 'fruits', 'الفواكه'
        HERBS = 'herbs', 'الأعشاب'

    class ProcessedFoodSubcategory(models.TextChoices):
        BEVERAGES = 'beverages', 'المشروبات'
        DAIRY_PRODUCTS = 'dairy_products', 'الألبان ومشتقاتها'
        SWEETS_AND_BAKERY = 'sweets_and_bakery', 'الحلويات والمخبوزات'
        MEAT_PRODUCTS = 'meat_products', 'منتجات لحوم'  
        FROZEN_FOODS = 'frozen_foods', 'أطعمة مجمدة'  

    class IndustrialSubcategory(models.TextChoices):
        CANNED_GOODS = 'canned_goods', 'المعلبات'
        SPICES_AND_HERBS = 'spices_and_herbs', 'التوابل والبهارات'

    class SpecialProductsSubcategory(models.TextChoices):
        ORGANIC = 'organic', 'عضوية'
        GLUTEN_FREE = 'gluten_free', 'خالية من الجلوتين'

    class MiscellaneousSubcategory(models.TextChoices):
        HONEY_AND_OILS = 'honey_and_oils', 'عسل وزيوت'
        OTHER = 'other', 'غير ذلك'
    
    @staticmethod
    def get_subcategories(category):
        if category == Product.ProductCategory.AGRICULTURAL_PRODUCTS:
            return [choice for choice in Product.AgriculturalSubcategory.choices]
        elif category == Product.ProductCategory.PROCESSED_FOOD:
            return [choice for choice in Product.ProcessedFoodSubcategory.choices]
        elif category == Product.ProductCategory.INDUSTRIAL_PRODUCTS:
            return [choice for choice in Product.IndustrialSubcategory.choices]
        elif category == Product.ProductCategory.SPECIAL_PRODUCTS:
            return [choice for choice in Product.SpecialProductsSubcategory.choices]
        elif category == Product.ProductCategory.MISCELLANEOUS:
            return [choice for choice in Product.MiscellaneousSubcategory.choices]
        return []
    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product-img/' ,blank=True )
    min_stock_alert = models.IntegerField(default=0)
    min_order_quantity = models.IntegerField(default=1)  
    unit = models.CharField(max_length=20, choices=Unit.choices)
    category = models.CharField(max_length=20, choices=ProductCategory.choices)
    subcategory = models.CharField(max_length=20, choices=[]) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subcategory_display(self):
        if self.category == self.ProductCategory.AGRICULTURAL_PRODUCTS:
            return self.AgriculturalSubcategory(self.subcategory).label
        elif self.category == self.ProductCategory.PROCESSED_FOOD:
            return self.ProcessedFoodSubcategory(self.subcategory).label
        elif self.category == self.ProductCategory.INDUSTRIAL_PRODUCTS:
            return self.IndustrialSubcategory(self.subcategory).label
        elif self.category == self.ProductCategory.SPECIAL_PRODUCTS:
            return self.SpecialProductsSubcategory(self.subcategory).label
        elif self.category == self.ProductCategory.MISCELLANEOUS:
            return self.MiscellaneousSubcategory(self.subcategory).label
        return self.subcategory