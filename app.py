from flask import Flask, render_template, request
from tutor import responder
from historial import cargar_historial, agregar_interaccion
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    pregunta_actual = None
    historial = cargar_historial()
    
    # Agregar timestamps al historial si no existen
    for item in historial:
        if 'timestamp' not in item:
            item['timestamp'] = datetime.now().strftime('%H:%M:%S')
    
    if request.method == 'POST':
        pregunta = request.form['pregunta']
        pregunta_actual = pregunta
        
        if pregunta.lower() != 'salir':
            # Obtener respuesta del tutor
            respuesta_texto = responder(pregunta)
            respuesta = respuesta_texto
            
            # Actualizar historial (ya se guarda en agregar_interaccion)
            historial = cargar_historial()
            # Agregar timestamp al último item
            if historial:
                historial[-1]['timestamp'] = datetime.now().strftime('%H:%M:%S')
    
    return render_template('index.html', 
                         respuesta=respuesta, 
                         historial=historial,
                         pregunta_actual=pregunta_actual)

if __name__ == '__main__':
    app.run(debug=True)