from gpiozero import LED, Button, TonalBuzzer, LightSensor
from random import choice
from time import sleep, time
 
 
# Asignacion de cada pin GPIO a un sensor
led_rojo = LED(20)
led_verde = LED(21)
led_azul = LED(26)
 
btn_rojo = Button(23, bounce_time = 0.1)
btn_verde = Button(22, bounce_time = 0.1)
btn_azul = Button(27, bounce_time = 0.1)
 
foto = Button(17)
buzzer = TonalBuzzer(18, octaves = 3)
 
 
# Generador clave
def modo_juego(repeticion):
    claves_con_repeticion = [['rojo', 'rojo', 'rojo'], ['rojo', 'rojo', 'verde'], ['rojo', 'rojo', 'azul'], ['rojo', 'verde', 'rojo'], ['rojo', 'verde', 'verde'], ['rojo', 'azul', 'rojo'], 
                             ['rojo', 'azul', 'azul'], ['verde', 'rojo', 'rojo'], ['verde', 'rojo', 'verde'], ['verde', 'verde', 'rojo'], ['verde', 'verde', 'verde'], ['verde', 'verde', 'azul'], 
                             ['verde', 'azul', 'verde'], ['verde', 'azul', 'azul'], ['azul', 'rojo', 'rojo'], ['azul', 'rojo', 'azul'],  ['azul', 'verde', 'verde'], ['azul', 'verde', 'azul'], 
                             ['azul', 'azul', 'rojo'], ['azul', 'azul', 'verde'], ['azul', 'azul', 'azul']]
 
    
    clave_sin_repeticion = [['rojo', 'verde', 'azul'], ['rojo', 'azul', 'verde'], ['verde', 'rojo', 'azul'], ['verde', 'azul', 'rojo'], ['azul', 'rojo', 'verde'], ['azul', 'verde', 'rojo']]
 
    if repeticion == "si":
        return choice(claves_con_repeticion)
 
    else:
        return choice(clave_sin_repeticion)
 
 
# Funcion que toca una melodia en el buzzer para cada situacion 
def toca_melodia(situacion):
    if situacion == "boton_correcto":
        notas = ['C5', 'E5', 'G5']
        tempo = [0.2, 0.2, 0.3]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
    elif situacion == "boton_incorrecto":
        notas = ['E5', 'C5', 'A4']
        tempo = [0.2, 0.2, 0.4]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
    elif situacion == "derrota":
        notas = ['G4', 'E4', 'C4']
        tempo = [0.3, 0.3, 0.6]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
    else:
        notas = ['C5', 'E5', 'G5', 'C6', 'G5']
        tempo = [0.2, 0.2, 0.2, 0.4, 0.4]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
 
# Funcion que compara cada boton presionado con cada termino de la clave
def comparador():
    global contador, ganaste, lista_btn, clave, tiempo_juego
    if contador == "" and len(lista_btn) == 1:
        if lista_btn[0] == clave[0]:
            print("\nsigue asi")
            toca_melodia("boton_correcto")
            contador = "paso1_completado"
        else:
            print("\nColor invalido. Intente de nuevo")
            toca_melodia("boton_incorrecto")
            lista_btn.clear()
            contador = ""
            tiempo_juego -= 1
            apaga_leds()
 
    if contador == "paso1_completado" and len(lista_btn) == 2:
        if lista_btn[1] == clave[1]:
            print("\nsigue asi")
            toca_melodia("boton_correcto")
            contador = "paso2_completado"
        else:
            print("\nColor invalido. Intente de nuevo")
            toca_melodia("boton_incorrecto")
            lista_btn.clear()
            contador = ""
            tiempo_juego -= 1
            apaga_leds()
    if contador == "paso2_completado" and len(lista_btn) == 3:
        if lista_btn[2] == clave[2]:
            ganaste = True
        else:
            print("\nColor invalido. Intente de nuevo")
            toca_melodia("boton_incorrecto")
            lista_btn.clear()
            contador = ""
            tiempo_juego -= 1
            apaga_leds()
 
 
# Funciones asociadas a cada boton
def activa_led_rojo():
    global lista_btn
    led_rojo.on()
    lista_btn.append("rojo")
    comparador()
 
def activa_led_verde():
    global lista_btn
    led_verde.on()
    lista_btn.append("verde")
    comparador()
 
def activa_led_azul():
    global lista_btn
    led_azul.on()
    lista_btn.append("azul")
    comparador()
 
 
# Funcion que apaga todos los leds
def apaga_leds():
    led_rojo.off()
    led_verde.off()
    led_azul.off()
 
 
# Desarrollo del juego
rejugar = True
while rejugar:
    tiempo_juego = int(input("TIEMPO TOTAL DE JUEGO: "))
    repeticion = str(input("DESEA PERMITIR QUE SE REPITA UN BOTON EN LA SECUENCIA: "))
 
    print("PRESIONA LA FOTORESISTENCIA PARA INICIAR EL JUEGO: ")
    foto.wait_for_release()
    print(f"EL JUEGO HA COMENZADO! TIENES {tiempo_juego} SEGUNDOS PARA ADIVINAR LA SECUENCIA")
 
    inicio = time()
    clave = modo_juego(repeticion)
    ganaste = False
    lista_btn = []
    contador = ""
 
    btn_rojo.when_pressed = activa_led_rojo
    btn_verde.when_pressed = activa_led_verde
    btn_azul.when_pressed = activa_led_azul
 
    while time() - inicio < tiempo_juego and ganaste == False:
        print(f"Tiempo restante: {tiempo_juego - (time() - inicio):.2f}", end="\r")
        sleep(1)
 
    if ganaste:
        print("\nGANASTE")
        toca_melodia("victoria")
        jugar_de_nuevo = str(input("DESEA VOLVER A JUGAR? ")).lower()
        if jugar_de_nuevo == "si":
            apaga_leds()
            rejugar = True
        else:
            apaga_leds()
            rejugar = False
 
    else:
        print("\nPERDISTE")
        toca_melodia("derrota")
        jugar_de_nuevo = str(input("DESEA VOLVER A JUGAR? ")).lower()
        if jugar_de_nuevo == "si":
            apaga_leds()
            rejugar = True
        else:
            apaga_leds()
            rejugar = False