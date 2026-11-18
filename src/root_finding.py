
def bisection(f, a, b, e, max_iterations=200):
    if f(a) * f(b) >= 0:
        print("Invalid interval")
        return None, 0

    iteration = 1
    c = a

    while iteration <= max_iterations:
        c = (a + b) / 2

        print("Iteration:", iteration)
        print("a =", a)
        print("b =", b)
        print("c =", c)
        print("f(c) =", f(c))
        print("--------------------")

        if abs(f(c)) < e:
            break

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

        iteration += 1

    print("Approximate root:", c)
    return c, iteration


def false_position(f, a, b, e, max_iterations=200):
    if f(a) * f(b) >= 0:
        print("Invalid interval")
        return None, 0

    iteration = 1
    c = a

    while iteration <= max_iterations:
        fl, fr = f(a), f(b)
        if abs(fr - fl) < 1e-15:
            break
            
        c = (a * fr - b * fl) / (fr - fl)

        print("Iteration:", iteration)
        print("a =", a)
        print("b =", b)
        print("c =", c)
        print("f(c) =", f(c))
        print("--------------------")

        if abs(f(c)) < e:
            break

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

        iteration += 1

    print("Approximate root:", c)
    return c, iteration


def newton_raphson(f, derivative, x, e, max_iterations=200):
    iteration = 1
    new_x = x

    while iteration <= max_iterations:
        deriv = derivative(new_x)
        if abs(deriv) < 1e-12:
            print("Derivative is zero")
            return None, 0

        current_x = new_x
        new_x = current_x - f(current_x) / deriv

        print("Iteration:", iteration)
        print("x =", current_x)
        print("New x =", new_x)
        print("f(x) =", f(new_x))
        print("--------------------")

        if abs(new_x - current_x) < e:
            break

        iteration += 1

    print("Approximate root:", new_x)
    return new_x, iteration


if __name__ == "__main__":
    # Test functions for standalone execution
    def f(x):
        return x**2 - 4

    def derivative(x):
        return 2*x

    print("\nBISECTION METHOD")
    root1, it1 = bisection(f, 1, 3, 0.0001)

    print("\nFALSE POSITION METHOD")
    root2, it2 = false_position(f, 1, 3, 0.0001)

    print("\nNEWTON RAPHSON METHOD")
    root3, it3 = newton_raphson(f, derivative, 3, 0.0001)

    print("\n========== METHOD COMPARISON ==========")

    results = [
        ("Bisection", root1),
        ("False Position", root2),
        ("Newton Raphson", root3)
    ]

    valid_results = []

    for method, root in results:
        if root is not None:
            error = abs(f(root))
            print(method)
            print("Root:", root)
            print("Error:", error)
            print("--------------------")
            valid_results.append((method, root, error))

    if valid_results:
        best = min(valid_results, key=lambda item: item[2])
        print("\n========== BEST RESULT ==========")
        print("Best Method:", best[0])
        print("Best Root:", best[1])
        print("Error:", best[2])