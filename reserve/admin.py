from django import forms
from django.contrib import admin

from reserve.models import Reserve, ReserveItem

class ReserveAdminForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ('status', 'user')


class ReserveItemsInLine(admin.TabularInline):
    model = ReserveItem
    extra = 1 #количество форм при добавлении нового заказа (по умолчанию было 3)

class TotalSumFilter(admin.SimpleListFilter):
    title = 'Фильтрация по сумме заказа'
    parameter_name = 'total_sum'

    def lookups(self, request, model_admin): #как в choices
        return (
            ('0to50000', 'от 0 до 50000'),
            ('50000to100000', 'от 50,000 до 100,000'),
            ('100000to150000', 'от 100,000 до 150,000'),
            ('from150000', 'от 150,000 и выше'),
        )
    def queryset(self, request, queryset): #список в листинге
        if self.value() == '0to50000':
            return queryset.filter(total_sum__lte=50000)
        elif self.value() == '50000to100000':
            return queryset.filter(total_sum__range=[50000, 100000])
        elif self.value() == '100000to150000':
            return queryset.filter(total_sum__range=[100000, 150000])
        elif self.value() == 'from150000':
            return queryset.filter(total_sum__gte=150000)
        else:
            return queryset


class ReserveAdmin(admin.ModelAdmin):
    inlines = [
        ReserveItemsInLine
    ]
    exclude = ('products', )
    form = ReserveAdminForm
    readonly_fields = ['user', 'total', 'created_at']
    list_display = ['id', 'status', 'total', 'created_at']
    list_filter = ['status', TotalSumFilter]
    search_fields = ['products__title']
    list_display_links = ['id', 'status']


    def save_model(self, request, obj, form, change): #change - change - true, create - false
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        total = 0
        for inline_form in formset:
            if inline_form.cleaned_data:
                price = inline_form.cleaned_data['product'].price
                quantity = inline_form.cleaned_data['quantity']
                total += price * quantity
        form.instance.total_sum = total
        form.instance.save()
        formset.save()

admin.site.register(Reserve, ReserveAdmin)
admin.site.register(ReserveItem)


#     model = Order
#     fields = ['product', 'quantity', 'price']
#     read_only_fields = ['product', 'quantity', 'price']
#     extra = 0
#
#     def products(self, instance):
#         return instance.order_items
#
#     def quantity(self, instance):
#         return instance.order_items.quantity
#
#     def price(self, instance):
#         return instance.order_items.price
#
#
# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemInLine]
#     exclude = ['items']
#     list_display = ('id', 'user', 'status', 'created_at', 'total_sum')


