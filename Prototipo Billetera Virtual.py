from datetime import datetime
import requests

endPoint = "https://api.binance.com"#url principal

def url(api):
    return endPoint+api

def valorCripto(cripto): #obtener informacion de la API
    return requests.get(url("/api/v3/ticker/price?symbol="+cripto))

def esCriptomoneda(cripto): #verificacion de criptomoneda a usar
    criptos = ["BTC","BCC","LTC","ETH","ETC","XRP"]
    if cripto in criptos:
        return True
    else:
        return False

estado1="Realizada"
estado2="Rechazada"
nombreCriptomoneda=None
seleccionMenu=None
estadoTranferencia=None
contenidoBilletera={"BTC":10,"BCC":2,"LTC":0,"ETH":0,"ETC":0,"XRP":0}
cantCriptoEnviar=0
cantCriptoRecivir=0
cantCriptofondear=0
totalDolares=0
historiaSalida=[]
historiaEntrada=[]
historiaFondeo=[]

codigoPropietario=input("para iniciar, por favor ingrese su codigo de usuario: ")
while not seleccionMenu=="7":
    seleccionMenu=input("Elija una opcion, marcando un numero del siguiente Menu: \n1-Recibir Transferencia \n2-Hacer Tranferencia  \n3-Conoce tu balance de una criptomoneda \n4-Balance general \n5-historial de transacciones \n6-Agregar fondos a tu billetera \n7-salir del programa \n")

    #Recibir Cripto
    if seleccionMenu=="1":
        codigoRemitente=input("Codigo de quien envia las criptomonedas: ")
        if codigoRemitente!=codigoPropietario:
            while not esCriptomoneda(nombreCriptomoneda):
                nombreCriptomoneda = input("¿criptomoneda a recibir?,\npor favor usar las siguientes abreviaciones BTC, BCC,LTC,ETH,ETC,XRP: ")
            cantCriptoRecivir=float(input("Cantidad de la criptomoneda a recibir: "))
            contenidoBilletera[nombreCriptomoneda] = contenidoBilletera[nombreCriptomoneda] + cantCriptoRecivir
            estadoTranferencia=estado1
            ahora= datetime.now (tz = None)
            fecha=ahora.strftime("%A, %d de %B de %Y a las %I:%M:%S%p")
        historiaEntrada.append([codigoRemitente,nombreCriptomoneda,cantCriptoRecivir,estadoTranferencia,fecha])
        nombreCriptomoneda=False

    #Enviar cripto
    if seleccionMenu=="2":
        codigoDestinatario=input("Codigo de quien recibe las criptomonedas: ")
        if codigoDestinatario!=codigoPropietario:
            while not esCriptomoneda(nombreCriptomoneda):
                nombreCriptomoneda = input("¿criptomoneda a Enviar?,\npor favor usar las siguientes abreviaciones BTC, BCC,LTC,ETH,ETC,XRP: ")
            cantCriptoEnviar=float(input("Cantidad de la criptomoneda a Enviar: "))
            if  cantCriptoEnviar>contenidoBilletera[nombreCriptomoneda]:
                print("Error: No cuentas con fondos suficientes para esta transferencia")
                estadoTranferencia=estado2
            else:
                contenidoBilletera[nombreCriptomoneda] = contenidoBilletera[nombreCriptomoneda] - cantCriptoEnviar
                estadoTranferencia=estado1
            ahora= datetime.now (tz = None)
            fecha=ahora.strftime("%A, %d de %B de %Y a las %I:%M:%S%p")
            historiaSalida.append([codigoDestinatario,nombreCriptomoneda,cantCriptoEnviar,estadoTranferencia,fecha])
            nombreCriptomoneda=False

    #Balance una Moneda
    if seleccionMenu=="3":
        while not esCriptomoneda(nombreCriptomoneda):
            nombreCriptomoneda = input("¿Criptomoneda a ver en tu Balance?,\npor favor usar las siguientes abreviaciones (BTC, BCC,LTC,ETH,ETC,XRP: ")
        datos = valorCripto(nombreCriptomoneda+"USDT").json()
        print("Actualmente tienes ",contenidoBilletera[nombreCriptomoneda], nombreCriptomoneda)
        print("El Valor en dolares de",nombreCriptomoneda,"es",datos["price"])
        cambio=float (datos["price"])
        valorDolares=contenidoBilletera[nombreCriptomoneda]*cambio
        print("Tus ",nombreCriptomoneda," te representan un saldo de ", valorDolares,"dolares")

    #Balance General
    if seleccionMenu=="4":
        print("Actualmente tienes en tu billetera: \n",contenidoBilletera)
        for nombreCriptomoneda in contenidoBilletera:
            datos = valorCripto(nombreCriptomoneda+"USDT").json()
            print("El Valor en dolares de",nombreCriptomoneda,"es",datos["price"])
            cambio=float (datos["price"])
            valorDolares=contenidoBilletera[nombreCriptomoneda]*cambio
            totalDolares=totalDolares+ valorDolares        
        print("Tus criptomonedas te representan un saldo total de ", totalDolares,"dolares")

    #Historial de transacciones
    if seleccionMenu=="5":
        print("Has Hecho las siguientes tranferencias de salida desde tu billetera: ")
        for salidas in historiaSalida:
            print(salidas)
        print("Has recibido las siguientes tranferencias a tu billetera: ")
        for entradas in historiaEntrada:
            print(entradas)
        print("Has realizado los siguientes depositos de tu parte a tu billetera: ")
        for fondos in historiaFondeo:
            print(fondos)
    
    #agregar fondos
    if  seleccionMenu=="6":
        while not esCriptomoneda(nombreCriptomoneda):
            nombreCriptomoneda = input("¿criptomoneda a agregar fondos?,\npor favor usar las siguientes abreviaciones BTC, BCC,LTC,ETH,ETC,XRP: ")
        cantCriptoFondear=float(input("Cantidad de la criptomoneda para agregar a tu billetera: "))
        contenidoBilletera[nombreCriptomoneda] = contenidoBilletera[nombreCriptomoneda] + cantCriptoFondear
        estadoTranferencia=estado1
        ahora= datetime.now (tz = None)
        fecha=ahora.strftime("%A, %d de %B de %Y a las %I:%M:%S%p")
        historiaFondeo.append(["Fondos Agregados",nombreCriptomoneda,cantCriptoFondear,estadoTranferencia,fecha])
        nombreCriptomoneda=False

    #Salida del programa
    if seleccionMenu=="7":
        exit()
    