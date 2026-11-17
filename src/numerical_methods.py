
def f(x):
    return x**2-4


def bisection(a,b,e):

    if f(a)*f(b)>=0:
        print("Invalid interval")
        return None

    iteration=1

    while True:

        c=(a+b)/2

        print("Iteration:",iteration)
        print("a =",a)
        print("b =",b)
        print("c =",c)
        print("f(c) =",f(c))
        print("--------------------")

        if abs(f(c))<e:
            break

        if f(a)*f(c)<0:
            b=c
        else:
            a=c

        iteration+=1

    print("Approximate root:",c)
    return c



def false_position(a,b,e):

    if f(a)*f(b)>=0:
        print("Invalid interval")
        return None

    iteration=1

    while True:

        c=(a*f(b)-b*f(a))/(f(b)-f(a))

        print("Iteration:",iteration)
        print("a =",a)
        print("b =",b)
        print("c =",c)
        print("f(c) =",f(c))
        print("--------------------")

        if abs(f(c))<e:
            break

        if f(a)*f(c)<0:
            b=c
        else:
            a=c

        iteration+=1

    print("Approximate root:",c)
    return c


def derivative(x):
    return 2*x


def newton_raphson(x,e):

    iteration=1

    while True:

        if derivative(x)==0:
            print("Derivative is zero")
            return None

        new_x=x-f(x)/derivative(x)

        print("Iteration:",iteration)
        print("x =",x)
        print("New x =",new_x)
        print("f(x) =",f(new_x))
        print("--------------------")

        if abs(new_x-x)<e:
            break

        x=new_x
        iteration+=1

    print("Approximate root:",new_x)
    return new_x


print("\nBISECTION METHOD")
root1=bisection(1,3,0.0001)

print("\nFALSE POSITION METHOD")
root2=false_position(1,3,0.0001)

print("\nNEWTON RAPHSON METHOD")
root3=newton_raphson(3,0.0001)


print("\n========== METHOD COMPARISON ==========")

results=[
    ("Bisection",root1),
    ("False Position",root2),
    ("Newton Raphson",root3)
]

valid_results=[]

for method,root in results:

    if root is not None:

        error=abs(f(root))

        print(method)
        print("Root:",root)
        print("Error:",error)
        print("--------------------")

        valid_results.append((method,root,error))


if valid_results:

    best=min(valid_results,key=lambda item:item[2])

    print("\n========== BEST RESULT ==========")
    print("Best Method:",best[0])
    print("Best Root:",best[1])
    print("Error:",best[2])