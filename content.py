import eel
from dataclasses import dataclass
from math import gcd
import sympy as sp

# Initialize Eel with the web folder
eel.init('web')

@dataclass
class X:
    num: int
    den: int
    pow: int

    def __post_init__(self):
        common_divisor = gcd(self.num, self.den)
        self.num //= common_divisor
        self.den //= common_divisor

    def add_coefs(self, other_num: int, other_den: int):
        new_num = self.num * other_den + other_num * self.den
        new_den = self.den * other_den
        common_divisor = gcd(new_num, new_den)
        self.num = new_num // common_divisor
        self.den = new_den // common_divisor

class Equation:
    def __init__(self):
        self.terms = []

    def add_x(self, x: X):
        for i, x_ in enumerate(self.terms):
            if x_.pow == x.pow:
                x_.add_coefs(x.num, x.den)
                if x_.num == 0:
                    self.terms.pop(i)
                return
        if x.num != 0:
            self.terms.append(x)

    def __str__(self):
        self.terms = sorted(self.terms, key=lambda x: -x.pow)
        return ' + '.join([f'{x.num}/{x.den}*n^{x.pow}' for x in self.terms])

    def evaluate(self, n: int) -> float:
        total = 0
        for term in self.terms:
            total += (term.num / term.den) * (n ** term.pow)
        return total

def calc_equation(q: int, verbose: bool) -> tuple:
    eq = Equation()
    eq.add_x(X(num=1, den=1, pow=1))  # Initialize with the term n^1
    verbose_steps = [f"Starting calculation with q = {q}"]
    final_eq = recursion(eq, 1, q, verbose_steps, verbose)
    return str(final_eq), verbose_steps

def recursion(prev_eq: Equation, q: int, target_q: int, verbose_steps: list, verbose: bool = False) -> Equation:
    new_eq = Equation()
    new_eq.add_x(X(num=1, den=1, pow=1))  # Start with the linear term (n^1)

    if verbose:
        verbose_steps.append(f"Step {q}: {prev_eq}")

    for term in prev_eq.terms:
        term_pow = term.pow
        new_eq.add_x(X(num=term.num * q, den=term.den * (term_pow + 1), pow=term_pow + 1))  # New power term
        new_eq.add_x(X(num=-term.num * q, den=term.den * (term_pow + 1), pow=1))  # Constant term

    if q == target_q:
        return new_eq
    else:
        return recursion(new_eq, q + 1, target_q, verbose_steps, verbose)

@eel.expose
def calculate_equation_and_solve(q, n, verbose):
    try:
        q = int(q)
        n = int(n)
        verbose = bool(verbose)

        equation_str, verbose_steps = calc_equation(q, verbose)
        
        eq = Equation()
        eq.add_x(X(num=1, den=1, pow=1))
        final_eq = recursion(eq, 1, q, [], False)
        result_at_n = final_eq.evaluate(n)

        verbose_steps.append(f"Final equation: {equation_str}")
        verbose_steps.append(f"Evaluation at n = {n}: {result_at_n}")

        return {"equation_str": equation_str, "verbose_steps": verbose_steps, "result": result_at_n}
    
    except ValueError:
        return {"equation_str": "Invalid input.", "verbose_steps": [], "result": None}

# Start the Eel app
eel.start('index.html')