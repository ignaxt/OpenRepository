##Decorador que valida que se Elija X o O

def validatorPlayer(valid_imput):
    def valid(option):
        if str(option).upper() not in ['X','O']:
            print('Jugador 1 Eligió ', option ,'. Esta no es una opcion válida')
            return
        return valid_imput(option)
    return valid

##Decorador que valida que las coordenadas elegidas son reales
def validatorBlock(valid_block):
    def validate(player,playerone,X,Y):
        player=player
        valoresposibles=[1,2,3] 
        if X not in valoresposibles:
            print('La opcion elegida no es valida (',X,',',Y,'), por favor ingrese un valor entre 1 y 3',
            ' para las opciones indicadas. Valores elegidos')
        if Y not in valoresposibles:
            print('La opcion elegida no es valida (',X,',',Y,'), por favor ingrese un valor entre 1 y 3',
            ' para las opciones indicadas. Valores elegidos')
        return valid_block(player,playerone,X,Y)
    return validate

##Validador de Ganador
def validateWinner(matriz):
    combinacionesganadoras=[[(1,1),(1,2),(1,3)],[(2,1),(2,2),(2,3)],[(3,1),(3,2),(3,3)],[(1,1),(2,1),(3,1)],
                [(1,2),(2,2),(3,2)],[(1,3),(2,3),(3,3)],[(1,1),(2,2),(3,3)],[(1,3),(2,2),(3,1)]]
    winner=False
    combinacionganador=[]
    combinacioniterar=[]
    values=[]
    while winner==False:
        for combinacion in combinacionesganadoras:
            values=[]
            combinacioniterar=[]
            for valores in combinacion:
                combinacioniterar.append(valores)
                values.append(matriz[valores[0]][valores[1]])
            if values[0]==values[1] and values[0]==values[2]:
                winner=True
                combinacionganador.append(combinacioniterar[0])
                combinacionganador.append(combinacioniterar[1])
                combinacionganador.append(combinacioniterar[2])
        winner=True
    return combinacionganador


def verTresenLinea(matriz):
    for i in matriz:
        print(i)


##creo la matriz
TresEnLinea=[
['[-]','[ 1 ]','[ 2 ]','[ 3 ]'],
['[1]','[ - ]','[ - ]','[ - ]'],
['[2]','[ - ]','[ - ]','[ - ]'],
['[3]','[ - ]','[ - ]','[ - ]']]
playeronemoves=[]
playertwomoves=[]
verTresenLinea(TresEnLinea)

@validatorPlayer
def ElegirOpcion(opcion):
    if str(opcion).upper() in ['X','O']:
        player=str(opcion).upper()
        print(player)
    return player

def InicioJuego():
    player=''
    while player not in ['X','O']:
        X=input('Jugador N° 1 Elija opción X u O : ')
        player=ElegirOpcion(X)

    print('El Jugador N° 1 Eligió ',X)
    return player 



def choseblock(player,playerone):
    inserted=False
    while inserted==False:
        X=int(input('Turno de {player} Elije un Ubicacion en eje Horizontal '.format(player=player)))
        Y=int(input('Turno de {player} Elije un Ubicacion en eje Vertical '.format(player=player)))
        print('Jugador {player} Eligio {X},{Y}'.format(player=player,X=X,Y=Y))
        inserted=insertValue(player,playerone,X,Y)

@validatorBlock
def insertValue(player,playerone,X,Y):
    toinsert=(int(X),int(Y))
    utilizado=False
    insertado=False
    if toinsert[0] not in [1,2,3] or toinsert[1] not in [1,2,3]:
        print(insertado)
    else:
        if toinsert in playeronemoves or toinsert in playertwomoves:
            utilizado=True
            print('El valor Horizontal {X} Vertical {Y} se encuentra utilizado. Por favor elija nuevamente'.format(X=toinsert[0],Y=toinsert[1]))
        else:
            if player==playerone:
                playeronemoves.append(toinsert)
                TresEnLinea[int(X)][int(Y)]='[ {player} ]'.format(player=player)
                insertado=True
            else:
                playertwomoves.append(toinsert)
                TresEnLinea[int(X)][int(Y)]='[ {player} ]'.format(player=player)
                insertado=True

    return insertado

def Game():
    playerone=''
    playertwo=''
    playerone=InicioJuego()
    if playerone=='X':
        playertwo='O'
        print('Jugador N° 2 es ',playertwo)
    else:
        playertwo='X'
        print('Jugador N° 2 es ',playertwo)

    gano=''
    winner=False
    Tie=False
    while winner==False:
        
        if len(playeronemoves)<=len(playertwomoves):
            choseblock(playerone,playerone)
        else:
            choseblock(playertwo,playerone)

        verTresenLinea(TresEnLinea)

        ganador=validateWinner(TresEnLinea)
        if len(ganador)==3:
            if (ganador[0] in playeronemoves and ganador[1] in playeronemoves and ganador[2] in playeronemoves):
                winner=True
                print ('El ganador es {player}'.format(player=playerone))
                gano=playerone
            if (ganador[0] in playertwomoves and ganador[1] in playertwomoves and ganador[2] in playertwomoves):
                winner=True
                print ('El ganador es {player}'.format(player=playertwo))
                gano=playertwo
        if '[ - ]' not in TresEnLinea[1] and '[ - ]' not in TresEnLinea[2] and '[ - ]' not in TresEnLinea[3] and winner==False:
            winner=True
            Tie=True
            gano='-'
    if gano=='-':
        print('El Resultado Final Ha sido un Empate')
    else:
        print('Felicitaciones {ganador} Haz sido el ganador'.format(ganador=gano))

Game()
    





