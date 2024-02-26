from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import os
from colorama import Fore, Style

def calcular_puntaje(resultado):
    if resultado == 'positiva':
        return 1
    elif resultado == 'negativa':
        return -1
    else:
        return 0


#función para leer el contenido de un archivo para entrenar el modelo
def leer_contenidoModelo(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        return file.read()


#función para leer el contenido de un archivo para clasificar
def leer_contenidoClasificar(archivo):
    carpeta = 'entrenamiento/nuevas'
    ruta_completa = os.path.join(carpeta, archivo)
    with open(ruta_completa, 'r', encoding='utf-8') as file:
        return file.read()


def listar_archivos_en_carpeta(carpeta):
    archivos = [archivo for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo))]
    return archivos

def entrenar_modelo():
    dir_buenas_noticias = 'entrenamiento/positivo'
    dir_malas_noticias = 'entrenamiento/negativo'

    archivos_buenas = [os.path.join(dir_buenas_noticias, archivo) for archivo in os.listdir(dir_buenas_noticias)]
    archivos_malas = [os.path.join(dir_malas_noticias, archivo) for archivo in os.listdir(dir_malas_noticias)]

    buenas_noticias = [leer_contenidoModelo(archivo) for archivo in archivos_buenas]
    malas_noticias = [leer_contenidoModelo(archivo) for archivo in archivos_malas]

    modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())
    X_train = buenas_noticias + malas_noticias
    y_train = ['positiva'] * len(buenas_noticias) + ['negativa'] * len(malas_noticias)
    modelo.fit(X_train, y_train)
    return modelo


def clasificar_noticias(modelo):
    carpeta = 'entrenamiento/nuevas'
    noticias = listar_archivos_en_carpeta(carpeta)

    res = 0
    # Leer el contenido de la nueva noticia
    for noticia in noticias:
        print(Fore.LIGHTYELLOW_EX + "[+] Noticia: " + Fore.YELLOW + f"{noticia}" + Style.RESET_ALL)

        nueva_noticia = leer_contenidoClasificar(noticia)

        # Clasificar la nueva noticia
        resultado = modelo.predict([nueva_noticia])

        res = res + calcular_puntaje(resultado)


        # Tomar una decisión basada en el resultado
        if resultado == 'positiva':
            # Colocar en la carpeta de noticias positivas
            print("[-] La noticia es: " + Fore.GREEN + "Positiva" + Style.RESET_ALL)
        elif resultado == 'negativa':
            # Colocar en la carpeta de noticias negativas
            print("[-] La noticia es: " + Fore.RED + "Negativa" + Style.RESET_ALL)

    return res


def menuEntrenamiento():
    modelo = entrenar_modelo()
    res = clasificar_noticias(modelo)
    res = res / len(listar_archivos_en_carpeta('entrenamiento/nuevas'))
    res_redondeado = round(res, 2)

    print(res_redondeado)

    return res_redondeado


if __name__ == "__main__":
    menuEntrenamiento()

