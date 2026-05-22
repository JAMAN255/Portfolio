from django.shortcuts import render
from .models import Calculations
# Create your views here.

def calculator(request):
    error_msg = None
    result = None
    if request.method == 'POST':
        try:
            float(request.POST.get("x"))
            float(request.POST.get("y"))

            if request.POST.get("operator") == '+':
                result = Calculations.add(float(request.POST.get("x")), float(request.POST.get("y")))
            elif request.POST.get("operator") == '-':
                result = Calculations.subtract(float(request.POST.get("x")), float(request.POST.get("y")))
            elif request.POST.get("operator") == '*':
                result = Calculations.multiply(float(request.POST.get("x")), float(request.POST.get("y")))
            elif request.POST.get("operator") == '/':
                if float(request.POST.get("y")) != 0:
                    result = Calculations.divide(float(request.POST.get("x")), float(request.POST.get("y")))
                else:
                    error_msg = "Cannot divide by zero."
            else:
                error_msg = "Invalid operation."
        except ValueError:
            error_msg = "Please enter valid numbers."
    return render(request, 'calculator/calculator.html', dict(error_msg=error_msg, result=result))
