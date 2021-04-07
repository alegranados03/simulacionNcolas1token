###########CONSTANTES############
NO_ELEGIBLE = 9999999999999
MC = 0
TTP = 6
MATRIZDERESULTADOS = []

def imprimirHeader(nodos):
    texto = '|{:^13s}|'.format("MC")
    for i in range(len(nodos)):
        texto += '{0:^13s}|{1:^13s}|{2:^13s}|'.format('Llegada {0}'.format(
            i+1), 'Salida {0}'.format(i+1), 'Cola {0}'.format(i+1))
    texto += '{0:^13s}|{1:^13s}|{2:^13s}|'.format(
        'pos. Token', 'timeout', 't. sig. nodo')
    print(texto)
#################################

##########CLASES ######################


class Nodo:
    def __init__(self, cLlegada, cSalida, tLlegada, cantidadCola):
        self.cLlegada = cLlegada
        self.cSalida = cSalida
        self.tLlegada = tLlegada
        self.cantidadCola = cantidadCola

    def __repr__(self):
        return str(self.__dict__)


class Token:
    def __init__(self, posicion, tOut, TOUT, TRUTEO, tSiguienteNodo):
        self.posicion = posicion
        self.tOut = tOut
        self.TOUT = TOUT
        self.TRUTEO = TRUTEO
        self.tSiguienteNodo = tSiguienteNodo

    def cambiarNodo(self, nodos):
        self.posicion = self.posicion + 1
        if(self.posicion == len(nodos)):
            self.posicion = 0

    def __repr__(self):
        return str(self.__dict__)

#################################################################


#############PROCEDIMIENTO#############################

# 1. seteamos los valores iniciales de los nodos

cantNodos = int(input('Ingrese la cantidad de nodos o colas del sistema: '))
nodos = []
for i in range(cantNodos):
    tiempoInicial = int(
        input('ingrese el tiempo inicial del nodo '+str(i+1)+': '))
    tiempoSalida = NO_ELEGIBLE
    tiempoLlegada = int(
        input('ingrese el tiempo de llegada al nodo '+str(i+1)+': '))
    cantidadCola = 0
    nodo = Nodo(tiempoInicial, tiempoSalida, tiempoLlegada, cantidadCola)
    nodos.append(nodo)
# [nodo1(cllegada,csalida),nodo2(cllegada,csalida),nodo3(cllegada,csalida)]

# 2. seteamos los valores iniciales del token
posicionInicial = 0
tOut = NO_ELEGIBLE
TOUT = 15
TRUTEO = 1
tSiguienteNodo = TRUTEO
token = Token(posicionInicial, tOut, TOUT, TRUTEO, tSiguienteNodo)


# 3. definimos cuantas iteraciones serán
iteraciones = int(input('ingrese la cantidad de iteraciones: '))

imprimirHeader(nodos)
# 4. comienzan las iteraciones
for i in range(iteraciones):
    texto = ''
    # 5. se revisa cual es el clock más pequeño de todos
    # [cllegada1,cllegada2,cllegada3]
    clocksLlegada = [nodo.cLlegada for nodo in nodos]
    # [csalida1,csalida2,csalida3]
    clocksSalida = [nodo.cSalida for nodo in nodos]
    # tOut = 0, tSiguienteNodo = 1
    clocksToken = [token.tOut, token.tSiguienteNodo]
    minimo = min([min(clocks)
                  for clocks in [clocksLlegada, clocksSalida, clocksToken]])
    MC = minimo

    # 5.1 se determina si fue entrada, salida, timeout o siguienteNodo
    # 5.1.1 Si es una entrada regresa su indice (nodo)
    entradas = []
    salidas = []
    arrtoken = []

    if(MC in clocksLlegada):
        entradas = [i for i in range(
            len(clocksLlegada)) if clocksLlegada[i] == MC]
    # 5.1.2 Si es una salida regresa su indice (nodo)
    if(MC in clocksSalida):
        salidas = [i for i in range(len(clocksSalida))
                   if clocksSalida[i] == MC]
    # 5.1.3 Si es clock del token regresa su indice (nodo)
    if(MC in clocksToken):
        arrtoken = [i for i in range(len(clocksToken)) if clocksToken[i] == MC]

    # 5.2 Para todas las entradas en MC = x
    for nodo in entradas:
        n = nodos[nodo]
        n.cLlegada = n.cLlegada + n.tLlegada
        n.cantidadCola = n.cantidadCola + 1

    # 5.3 Para todas las salidas en MC = x
    for nodo in salidas:
        n = nodos[nodo]
        n.cantidadCola = n.cantidadCola - 1
        n.cSalida = NO_ELEGIBLE
        if(n.cantidadCola > 0):
            if(MC < clocksToken[0]):
                n.cSalida = MC + TTP
        else:
            token.tOut = NO_ELEGIBLE
            token.tSiguienteNodo = MC + TRUTEO

    # 5.4 Para eventos de token
    for clock in arrtoken:
        # 5.4.1 Para evento de TIMEOUT
        if(clock == 0):
            salidaNodo = nodos[token.posicion].cSalida
            if(token.tOut < salidaNodo and salidaNodo != NO_ELEGIBLE):
                token.tOut = salidaNodo
            else:
                token.tOut = NO_ELEGIBLE
                token.tSiguienteNodo = MC + TRUTEO

        # 5.4.2 para evento LLEGADA AL SIGUIENTE NODO
        if(clock == 1):
            token.tSiguienteNodo = MC + 1
            token.cambiarNodo(nodos)
            # CUANDO EL TOKEN SE MUEVE A UN NODO
            if(nodos[token.posicion].cantidadCola > 0):
                n = nodos[token.posicion]
                n.cSalida = MC + TTP
                token.tOut = MC + token.TOUT
                token.tSiguienteNodo = NO_ELEGIBLE

    resultado = []
    resultado.append([MC])
    texto += '|{0:13d}|'.format(MC)
    for nodo in nodos:
        resultado.append([nodo.cLlegada, nodo.cSalida, nodo.cantidadCola])
        texto += '{0:13d}|{1:13d}|{2:13d}|'.format(
            nodo.cLlegada, nodo.cSalida, nodo.cantidadCola)
    resultado.append([token.posicion, token.tOut, token.tSiguienteNodo])
    texto += '{0:13d}|{1:13d}|{2:13d}|'.format(
        token.posicion, token.tOut, token.tSiguienteNodo)
    print(texto)
    MATRIZDERESULTADOS.append(resultado)

print("\n\n\n")

for row in MATRIZDERESULTADOS:
    fix = []
    for array in row:
        for el in array:
            fix.append(el)



