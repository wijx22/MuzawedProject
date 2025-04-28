from django import forms

from .models import Branch, Supplier, SupplyRequest, CommercialInfo


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "logo",
            "supply_sector",
            "delivery_service",
            "order_lead_time_days",
            "is_available",
            "unavailable_from",
            "unavailable_to",
            "fast_service_details",
            "late_payment_options",
            "supply_days",
        ]
        widgets = {
            "unavailable_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "unavailable_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["city"]




class CommercialInfoForm(forms.ModelForm):
    class Meta:
        model = CommercialInfo
        exclude = ['supplier'] 

class SupplyRequestForm(forms.ModelForm):
    class Meta:
        model = SupplyRequest
        exclude = ['reason', 'status']  
