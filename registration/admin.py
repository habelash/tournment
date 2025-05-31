from django.contrib import admin
from .models import TournamentRegistration
from .models import Payment

# Register your models here.
admin.site.register(TournamentRegistration)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('registration', 'order_id', 'txn_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'txn_id', 'registration__player_name')
