def generate_equation():
    parameter1 = random.randint(-10, 10)
    parameter2 = random.randint(-10, 10)
    parameter3 = random.randint(-10, 10)

    equation = f"{parameter1} * x + {parameter2} = {parameter3}"
    return equation, parameter1, parameter2, parameter3