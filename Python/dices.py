from random import random
from re import U
from tkinter import N

from sqlalchemy import false 

def roll_dice():
    """
        Devuelve el un valor aleatorio de 1 a 6
    """
    a=0
    a=int((random()*10%6)+1)
    return a

def sum_dices(dice1,dice2):
    """
        Devuelve la suma de los dos dados pasados por parametro
    """
    suma=int(dice1) + int(dice2)
    return suma

def validate_answer(answer):
    """
        Funcion que valida que la respuesta sea correcta y devuelve true or false
    """
    response=True
    if str.capitalize(answer) not in ['Y','N']:
        response=False
    return response

def wanna_play():
    """
        Función que valida si el jugador desea jugar
    """
    play=False
    answer=input("Ingrese su respuesta: y = yes o n = no  ")
    while play==False:
        if validate_answer(answer)==False:
            print("Por favor ingrese una opción válidad: y = yes o n = no \n")
            answer=input("Ingrese su respuesta: y = yes o n = no  ")
        elif str.capitalize(answer)=='Y':
            play=True
        else:
            play=False
            return play
            break
    return play

def play():
    """
        Juego de Dados
    """
    print("Bienvenidos al juego de Dados, Deseas Jugar: y = yes n = no  ")
    play=False
    play=wanna_play()

    while play==True:
        print("Se arrojan los Dados")
        dice1=roll_dice()
        dice2=roll_dice()
        suma=sum_dices(dice1,dice2)
        print("El valor del dado uno es {dice1} , el valor del dado dos es {dice2}".format(dice1=dice1,dice2=dice2))
        print("Felicitaciones, has sumado {suma} puntos".format(suma=suma))
        print("\n")
        print("Quieres Arrojar los dados nuevamente")
        play=wanna_play()
        
    print("Muchas gracias por Jugar! :)")

play()
