#!/usr/bin/env python3
"""
Module for calculating discriminant of quadratic equation.
Quadratic equation: ax² + bx + c = 0
Discriminant: D = b² - 4ac
"""


def calculate_discriminant(a: float, b: float, c: float) -> float:
    """
    Calculate discriminant for quadratic equation.
    
    Args:
        a: Coefficient for x²
        b: Coefficient for x
        c: Constant term
    
    Returns:
        float: Discriminant value
    
    Raises:
        ValueError: If a is zero (not a quadratic equation)
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in quadratic equation")
    
    return b**2 - 4*a*c


def solve_quadratic(a: float, b: float, c: float) -> tuple:
    """
    Solve quadratic equation and return roots.
    
    Args:
        a: Coefficient for x²
        b: Coefficient for x
        c: Constant term
    
    Returns:
        tuple: Roots of the equation
    """
    discriminant = calculate_discriminant(a, b, c)
    
    if discriminant < 0:
        return ()  # No real roots
    elif discriminant == 0:
        root = -b / (2 * a)
        return (root,)
    else:
        root1 = (-b + discriminant**0.5) / (2 * a)
        root2 = (-b - discriminant**0.5) / (2 * a)
        return (root1, root2)


if __name__ == "__main__":
    # Example usage
    try:
        a, b, c = 1, -3, 2
        discriminant = calculate_discriminant(a, b, c)
        roots = solve_quadratic(a, b, c)
        
        print(f"Equation: {a}x² + {b}x + {c} = 0")
        print(f"Discriminant: {discriminant}")
        print(f"Roots: {roots}")
        
    except ValueError as e:
        print(f"Error: {e}")
#Ошибка
#def bad_function():
#x=1  # Ошибка: нет отступов!
#print("no indent")  # Тоже нет отступа!

#very_long_variable_name_that_is_way_too_long_and_violates_pep8_guidelines_so_much = 1  # Слишком длинная строка

#def another_bad_function(  x , y  ):  # Лишние пробелы
   # unused = 123  # Неиспользуемая переменная
   # return True