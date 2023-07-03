from asyncio import format_helpers
from django.contrib import admin
from .models import Order, OrderItem, DeliveryMethod

from openpyxl import Workbook
from django.http import HttpResponse
from datetime import date


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'status',
                    'created_at', 'total_price', 'payment')
    list_display_links = ('id', 'first_name')
    list_filter = ('status', 'payment')

    actions = ['export_to_excel']

    def export_to_excel(modeladmin, request, queryset):
        """Формирование отчетов по заказам"""
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{date.today()}.xlsx"'

        wb = Workbook()
        ws = wb.active

        # Заголовки таблицы
        columns = [['Статус', 'Имя', 'Фамилия', 'Почта', 'Телефон', 'Адрес', 'Город', 'Примечание', 'Сумма(рубли)',
                    'Дата создания', 'Дата обновления', 'Дата доставки', 'Способ доставки', 'Оплата', 'Товары']]

        for item in queryset:
            string = ''
            if item.user:
                items = OrderItem.objects.filter(order__user=item.user)
            else:
                items = OrderItem.objects.filter(
                    order__session_id=item.session_id)
            for order_item in items:
                string += order_item.product.title+','

            columns.append([item.get_status_display(), item.first_name, item.last_name, item.email, item.phone, item.address, item.city, item.note_order,
                           item.total_price, item.created_at.date(), item.updated_at.date(), item.delivery_date, f'{item.delivery_method}', 'Да' if item.payment else 'Нет', string])

        for row in columns:
            ws.append(row)

        wb.save(response)
        return response
    export_to_excel.short_description = "Экспортировать в Excel"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_display_links = ('id', 'order')
    list_filter = ('order',)


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
