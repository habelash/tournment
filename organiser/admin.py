# admin.py
from django.contrib import admin
from .models import Expense
from django.utils.html import format_html


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'category', 'date', 'receipt_link']
    readonly_fields = ['receipt_link']

    def receipt_link(self, obj):
        if obj.receipt:
            return format_html("<a href='{}' target='_blank'>View Receipt</a>", obj.receipt.url)
        return "No Receipt"
    receipt_link.allow_tags = True
    receipt_link.short_description = 'Receipt'