
def gauss_elimination(A):

    n=len(A)

    # Forward Elimination
    for i in range(n):

        # Find the largest pivot
        pivot=i

        for j in range(i+1,n):
            if abs(A[j][i])>abs(A[pivot][i]):
                pivot=j

        # Swap rows
        A[i],A[pivot]=A[pivot],A[i]

        if abs(A[i][i])<1e-12:
            print("No unique solution")
            return None

        # Make elements below pivot zero
        for j in range(i+1,n):

            factor=A[j][i]/A[i][i]

            for k in range(i,n+1):
                A[j][k]=A[j][k]-factor*A[i][k]

    # Back Substitution
    x=[0]*n

    for i in range(n-1,-1,-1):

        total=0

        for j in range(i+1,n):
            total+=A[i][j]*x[j]

        x[i]=(A[i][n]-total)/A[i][i]

    return x


def gauss_jordan(A):

    n=len(A)

    for i in range(n):

        pivot=i

        for j in range(i+1,n):
            if abs(A[j][i])>abs(A[pivot][i]):
                pivot=j

        A[i],A[pivot]=A[pivot],A[i]

        if abs(A[i][i])<1e-12:
            print("No unique solution")
            return None

        divisor=A[i][i]

        for k in range(n+1):
            A[i][k]=A[i][k]/divisor

        for j in range(n):

            if j!=i:

                factor=A[j][i]

                for k in range(n+1):
                    A[j][k]=A[j][k]-factor*A[i][k]

    x=[0]*n

    for i in range(n):
        x[i]=A[i][n]

    return x

if __name__=="__main__":

    A=[
        [2,1,1,10],
        [3,2,1,14],
        [1,2,3,14]
    ]

    B=[
        [2,1,1,10],
        [3,2,1,14],
        [1,2,3,14]
    ]

    result=gauss_elimination(A)

    if result is not None:
        print("\nGAUSS ELIMINATION")
        print("x =",result[0])
        print("y =",result[1])
        print("z =",result[2])

    result=gauss_jordan(B)

    if result is not None:
        print("\nGAUSS-JORDAN METHOD")
        print("x =",result[0])
        print("y =",result[1])
        print("z =",result[2])

