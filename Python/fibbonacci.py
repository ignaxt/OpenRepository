def fib(numero):
    arg=[0,1]
    i=0
    while i<=numero-2:
        a=arg[len(arg)-2]
        b=arg[len(arg)-1]
        arg.append(a + b)
        i+=1
    return arg

print(fib(35))


#Bucle for

def tabla_multiplicar(numero):
    "Imprime la tabla de multiplicar"
    for indice in [1,2,3,4,5,6,7,8,9,10]:
        print(f"{numero} * {indice} = {numero * indice}")

tabla_multiplicar(5)

def imprimir_todasTablas():
    "imprime todos los numeros multiplicados"
    for i in range(1,11):
        for j in range(1,11):
            print(f"{i} * {j} = {i*j}")

imprimir_todasTablas()

def sumarPares(numero):
    "Imprime la sumatoria de los pares desde el 2 hasta el número pasado por parametro"
    c=0
    for i in range(2,numero+1,2):
        #if i%2==0:
            c+=i
    return c

print(sumarPares(100))

