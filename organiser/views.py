from django.shortcuts import render, redirect
from .expenses import ExpenseForm
from django.contrib.auth.decorators import login_required
from .models import Expense


def expenses(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses.html', {'expenses': expenses})