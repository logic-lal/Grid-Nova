
def euler_method(f,x0,y0,h,x_end):

    x=x0
    y=y0

    results=[]

    while x<x_end:

        results.append((x,y))

        slope=f(x,y)

        y=y+h*slope
        x=x+h

    results.append((x,y))

    return results


# Test Euler's Method
def f(x,y):
    return x+y


result=euler_method(f,0,1,0.1,0.2)

print("\nEULER'S METHOD")

for x,y in result:
    print("x =",round(x,2),"y =",round(y,4))



def modified_euler(f,x0,y0,h,x_end):

    x=x0
    y=y0

    results=[]

    while x<x_end:

        results.append((x,y))

        k1=f(x,y)

        yp=y+h*k1

        k2=f(x+h,yp)

        y=y+(h/2)*(k1+k2)

        x=x+h

    results.append((x,y))

    return results


# Test Modified Euler
result=modified_euler(f,0,1,0.1,0.2)

print("\nMODIFIED EULER METHOD")

for x,y in result:
    print("x =",round(x,2),"y =",round(y,4))
