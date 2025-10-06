#Miniproyecto 1. Actividad 1
from gpiozero import LED, Button, TonalBuzzer
from time import sleep
from random import choice, randint
import urllib.request, json
 
 
#Pines GPIO de cada sensor
red = LED(20)
green = LED (21)
blue = LED(26)
btn1 = Button(23)
btn2 = Button(22)
btn3 = Button(27)
btn4 = Button(17)
btn5 = Button(18)
 
buzzer = TonalBuzzer(4)
 
 
#Funcion que asigna una melodias al buzzer
def melodia_buzzer(str):
    if str == "letra_correcta":
        notas = ["C5","E5","G5"]
        tempo = [0.5, 0.5, 1]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
    elif str == "letra_incorrecta":
        notas = ['E5', 'D#5', 'D5', 'C#5', 'C5', 'B4']
        tempo = [0.15, 0.15, 0.15, 0.15, 0.2, 0.3]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
    elif str == "victoria":
        notas = ["C5","E5","G5","C6","G5","E5","C5","G4"]
        tempo = [0.5, 0.5, 1, 1, 0.5, 0.5, 1, 2]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
    else:
        notas = ["E5","C5","A4","F4"]
        tempo = [0.5, 0.5, 1, 2]
        for i in range(len(notas)):
            buzzer.play(notas[i])
            sleep(tempo[i])
            buzzer.stop()
            sleep(0.1)
 
 
#Funciones asociadas a cada boton
def press_button1():
    global btn
    btn = "1"
    return btn
 
def press_button2():
    global btn
    btn = "2"
    return btn
 
def press_button3():
    global btn
    btn = "3"
    return btn
 
def press_button4():
    global btn
    btn = "4"
    return btn
 
def press_button5():
    global btn
    btn = "5"
    return btn
 
 
#Cuerpo del programa
alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n','ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','-']
 
historial_letras = []
 
pos = 0
btn = 0
contador = 0
def abecedario(progreso, intentos):
    global pos, btn, contador, historial_letras
 
    with open("racha.txt", "w", encoding="utf-8") as f:
                f.write(str(contador))
 
    with open("racha.txt", "r", encoding="utf-8") as f:
        racha = f.read()
 
    print(f"Racha historica de victorias: {racha} ")
    print("Palabra actual:", " ".join(progreso))
    print(f"Intentos restantes: {intentos}")
    print(f"Letra actual: {alfabeto[pos].upper()}")
    if len(historial_letras) > 0:
        print("Letras usadas hasta ahora:", ", ".join(historial_letras).upper())
    print("Presione boton: ")
    print("1: Siguiente | 2:Anterior | 3: +5 | 4: -5 | 5: Seleccionar")
    print("\n")
 
    btn1.when_pressed = press_button1
    btn2.when_pressed = press_button2
    btn3.when_pressed = press_button3
    btn4.when_pressed = press_button4
    btn5.when_pressed = press_button5
 
    while True:
        if btn == 0:
            sleep(1)
        else:
            if btn == "1":
                pos = (pos + 1) % 28
            elif btn == "2":
                pos = (pos - 1) % 28
            elif btn == "3":
                pos = (pos + 5) % 28
            elif btn == "4":
                pos = (pos - 5) % 28
            elif btn == "5":
                historial_letras.append(alfabeto[pos])
                btn = 0
                break
 
            print(f"Racha historica de victorias: {racha}")
            print("Palabra actual:", " ".join(progreso))
            print(f"Intentos restantes: {intentos}")
            print(f"Letra actual: {alfabeto[pos].upper()}")
 
            if len(historial_letras) > 0:
                print("Letras usadas hasta ahora:", ", ".join(historial_letras).upper())
 
            print("Presione boton: ")
            print("1: Siguiente | 2:Anterior | 3: +5 | 4: -5 | 5: Seleccionar")
            print("\n")
            btn = 0
 
 
def validador(linf,lsup,mensaje):
    x = int(input(mensaje))
    while x < linf or x > lsup:
        print("Error. Ingrese un valor dentro del rango")
        x = int(input(mensaje))
    return x
 
 
def dificultad(palabra_objetivo):
    global contador
    intentos = validador(1,5,"Numero de intentos (maximo 5): ")
    print("\n")
    progreso = ["_"]*len(palabra_objetivo)
 
    while intentos > 0:
        if intentos == 5:
            red.off()
            green.off()
            blue.on()
 
        elif intentos == 3 or intentos == 4:
            red.off()
            green.on()
            blue.off()
 
        else:
            red.on()
            green.off()
            blue.off()
 
        abecedario(progreso,intentos)
        letra_candidata = alfabeto[pos]
        if letra_candidata in palabra_objetivo and " ".join(progreso) != palabra_objetivo:
            print("Fantastico! Sigue asi")
            melodia_buzzer("letra_correcta")
            for i in range(len(palabra_objetivo)):
                if palabra_objetivo[i] == letra_candidata:
                    progreso[i] = letra_candidata
        else:
            intentos -= 1
            print(f"No te rindas! Por favor, continua")
            melodia_buzzer("letra_incorrecta")
 
        if "".join(progreso) == palabra_objetivo:
            contador += 1
            with open("racha.txt", "w", encoding="utf-8") as f:
                f.write(str(contador))
            print(f"Has ganado! La palabra era: {palabra_objetivo}")
            melodia_buzzer("victoria")
            break
 
    if intentos == 0:
            contador = 0
            with open("racha.txt", "w", encoding="utf-8") as f:
                f.write(str(contador))
 
            print(f"Has perdido! La palabra era: {palabra_objetivo}. No te deprimas! Vuelve a intentarlo")
            print("\n")
            melodia_buzzer("derrota")
 
 
# Github palabras
SPANISH_WORDS_URL = "https://raw.githubusercontent.com/words/an-array-of-spanish-words/master/index.json"
 
spanish_words = []
 
def load_spanish_words():
    global spanish_words
    print("Fetching Spanish word list from the internet...")
 
    with urllib.request.urlopen(SPANISH_WORDS_URL, timeout=5) as response:
        data = response.read()
        words = json.loads(data)
        spanish_words = [w.strip().lower() for w in words if isinstance(w, str) and w.strip()]
 
    print(f"Loaded {len(spanish_words)} words from online source!")
 
def get_random_spanish_word_by_length(length):
    global spanish_words
 
    if not spanish_words:
        load_spanish_words()
 
    filtered = [w for w in spanish_words if len(w) == length]
 
    if not filtered:
        raise ValueError(f"No Spanish words found with length {length}")
 
    return choice(filtered)
 
def get_spanish_pokemon_name(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"
 
    with urllib.request.urlopen(url, timeout=5) as response:
        raw_data = response.read()
        data = json.loads(raw_data)
 
        for item in data["names"]:
            if item["language"]["name"] == "es":
                return item["name"].lower()
 
        return data["name"].lower()
 
def get_random_spanish_pokemon(max_id=1010):
    pid = randint(1, max_id)
    return get_spanish_pokemon_name(pid)
 
 
#Interfaz del usuario
aux = False
while aux == False:
    modo = str(input("SELECCIONE MODO DE JUEGO (POKEMON o NORMAL): ")).lower()
    if modo == "pokemon":
        palabra_objetivo = get_random_spanish_pokemon()
        dificultad(palabra_objetivo)
        jugar_de_nuevo = str(input("Desea empezar una nueva partida: ")).lower()
        if jugar_de_nuevo == "si":
            historial_letras = []
            pos = 0
            aux = False
        else:
            aux = True
 
    elif modo == "normal":
        try:
            longitud_palabra = int(input("Cantidad de letras deseada en la palabra: "))
            palabra_objetivo = get_random_spanish_word_by_length(longitud_palabra)
            dificultad(palabra_objetivo)
            jugar_de_nuevo = str(input("Desea empezar una nueva partida: ")).lower()
            if jugar_de_nuevo == "si":
                historial_letras = []
                pos = 0
                aux = False
            else:
                aux = True
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print("Error fetching word:", e)
 
    else:
        print("MODO DE JUEGO INVALIDO. POR FAVOR, SELECCIONA 'POKEMON' o 'NORMAL'")