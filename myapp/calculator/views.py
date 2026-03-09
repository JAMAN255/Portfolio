from django.shortcuts import render
from .models import Calculations, IndexCalculations
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

def index_calculator(request):
    error_msg = None
    ageing_result = None
    sauvy_result = None
    ec_weight_result = None
    if request.method == 'POST':
        try:
            request.POST.get("first_ec_gen")
            request.POST.get("second_ec_gen")
            request.POST.get("third_ec_gen")
            request.POST.get("first_bg_gen")
            request.POST.get("second_bg_gen")
            request.POST.get("third_bg_gen")

            index_calculations = IndexCalculations(
                first_ec_gen=request.POST.get("first_ec_gen"),
                second_ec_gen=request.POST.get("second_ec_gen"),
                third_ec_gen=request.POST.get("third_ec_gen"),
                first_bg_gen=request.POST.get("first_bg_gen"),
                second_bg_gen=request.POST.get("second_bg_gen"),
                third_bg_gen=request.POST.get("third_bg_gen")
            )

            ageing_result = index_calculations.ageing_idx()
            sauvy_result = index_calculations.sauvy_idx()
            ec_weight_result = index_calculations.ec_weight_idx()

        except ValueError:
            error_msg = "Please enter valid set of numbers."
    return render(request, 'calculator/index_calculator.html', dict(error_msg=error_msg, ageing_result=ageing_result, sauvy_result=sauvy_result, ec_weight_result=ec_weight_result))