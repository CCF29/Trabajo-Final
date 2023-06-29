#-----------Importando libreria----------
import cv2

#----------Realizamos la videoCaptura----------
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#---------Creamos nuestro While True----------
while True:

    #Realizamos la lectura de la VideoCaptura
    ret, frame = cap.read()

    if ret == False:
        break

    #Extraemos el ancho y el alto de los fotogramas
    al, an, c = frame.shape
    # print(al,an)

    # Tomar el centro de la imagen
    # En x
    x1 = int(an / 3)  # Tomamos el 1/3 de la imagen
    x2 = int(x1 * 2)  # Hasta el inicio del 3/3 de la imagen

    # En y
    y1 = int(al / 3)  # Tomamos el 1/3 de la imagen
    y2 = int(y1 * 2)  # Hasta el inicio del 3/3 de la imagen

    # Texto
    cv2.putText(frame, 'Ubique su ojo en el rectangulo', (x1 - 50, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Ubicamos el rectangulo en las zonas extraidas
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    #Realizamo un recorte a nuestra zona de interes
    recorte = frame[y1:y2, x1:x2]

    # Pasamos el recorte a escala de grises
    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)

    # Aplicaremos un filtro Gaussiano para eliminar las pestañas
    gris = cv2.GaussianBlur(gris, (3, 3), 0)  # Entre mayor sea el kernel mas se desenfoca

    # Aplicaremos un umbral para detectar la pupila por el color
    _, umbral = cv2.threshold(gris, 7, 255, cv2.THRESH_BINARY_INV)

    # Extaremos los contornos de la zona seleccionada
    contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(contornos)

    # Vamos a extraer el area de los contornos
    # Primero los ordenamos del mas grande al mas pequeño
    contornos = sorted(contornos, key=lambda x: cv2.contourArea(x), reverse=True)

    #Dibujamos los contornos extraidos
    for contorno in contornos:
        #Dibujamos el contorno
        #cv2.drawContours(recorte, [contorno], -1, (0,255,0), 2)

        #Dibujamos un rectangulo a partir del contorno
        #Extraemos las coordenadas
        (x, y, ancho, alto) = cv2.boundingRect(contorno)
        #Dibujamos
        cv2.rectangle(frame,(x + x1, y + y1), (x + ancho + x1, y + alto + y1), (0,255,0), 1)

        #Mostramos dos lineas a partir del centro del ojo
        #Eje y
        cv2.line(frame, (x1 + x + int(ancho/2), 0), (x1+ x + int(ancho/2), al), (0,0,255), 1)
        #Eje x
        cv2.line(frame, (0, y1 + y + int(ancho/2)), (an, y1 + y + int(ancho/2)), (0, 0, 255), 1)
        break


    #Mostramos el recorte en gris
    cv2.imshow("Ojos", frame)

    #Mostramos el recorte
    cv2.imshow("Recorte", recorte)

    #Mostramos el umbral
    cv2.imshow("Umbral", umbral)

t = cv2.waitkey(1)

cap.release()
cv2.destroyAllWindows()