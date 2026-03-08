from django.shortcuts import render
from . import models
# Create your views here.

def calculator(request):
    error_msg = None
    result = None
    if request.method == 'POST':
        try:
            float(request.POST["a"])
            float(request.POST["b"])

            if request.POST["operator"] == '+':
                result = models.add(float(request.POST["a"]), float(request.POST["b"]))
            elif request.POST["operator"] == '-':
                result = models.subtract(float(request.POST["a"]), float(request.POST["b"]))
            elif request.POST["operator"] == '*':
                result = models.multiply(float(request.POST["a"]), float(request.POST["b"]))
            elif request.POST["operator"] == '/':
                if float(request.POST["b"]) != 0:
                    result = models.divide(float(request.POST["a"]), float(request.POST["b"]))
                else:
                    error_msg = "Cannot divide by zero."
            else:
                error_msg = "Invalid operation."
        except ValueError:
            error_msg = "Please enter valid numbers."
    return render(request, 'calculator/calculator.html', dict(error_msg=error_msg, result=result))