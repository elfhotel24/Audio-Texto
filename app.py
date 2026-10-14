"""
DESCRIPCIÓN GENERAL:
Aplicación web que permite convertir archivos de audio (MP3/WAV) a texto,
visualizar su representación en código máquina y encriptar/desencriptar
el texto resultante usando codificación Base64.
"""
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS

import os
import binascii
import base64
import io
import speech_recognition as sr
import librosa
import soundfile as sf
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


# SECCIÓN 2: CONFIGURACIÓN INICIAL DE FLASK

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_segura_proyecto_audio'  # Clave para sesiones
app.config['UPLOAD_FOLDER'] = 'uploads'                   # Carpeta para archivos subidos
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}         # Formatos permitidos
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024       # Límite: 10MB por archivo

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Variable global para mantener el estado de la aplicación
estado_actual = {
    'archivo': None,           # Nombre del archivo cargado
    'codigo_maquina': None,    # Representación hexadecimal
    'texto': None,             # Texto transcrito
    'texto_encriptado': None,  # Texto en Base64
    'error': None              # Mensajes de error
}


# SECCIÓN 3: FUNCIONES DE VALIDACIÓN Y CONVERSIÓN

def es_audio_permitido(filename):
    """Verifica si la extensión del archivo es .wav o .mp3"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def leer_codigo_maquina(ruta):
    """Convierte los primeros bytes del archivo a representación hexadecimal"""
    try:
        with open(ruta, 'rb') as f:
            datos = f.read(512)  # Lee solo 512 bytes para visualización
            hex_str = binascii.hexlify(datos).decode('utf-8').upper()
            # Formatea en grupos de 4 caracteres para mejor lectura
            return ' '.join([hex_str[i:i+4] for i in range(0, len(hex_str), 4)])
    except Exception as e:
        return f"Error: {str(e)}"


def convertir_audio_a_texto(ruta):
    """
    Convierte archivos MP3/WAV a texto usando Google Speech Recognition.
    Procesa máximo 60 segundos (límite de la API gratuita).
    """
    try:
        # Cargar audio con librosa (soporta MP3 )
        audio_data, sample_rate = librosa.load(
            ruta, 
            sr=None,      # Mantener frecuencia original
            mono=True,    # Convertir a mono para mejor reconocimiento
            duration=60   # Límite de 60 segundos (API Google)
        )
        
        # Convertir a formato WAV en memoria (requerido por speech_recognition)
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, sample_rate, format='WAV')
        buffer.seek(0)  # Rebobinar al inicio del buffer
        
        # Realizar reconocimiento de voz
        reconocedor = sr.Recognizer()
        with sr.AudioFile(buffer) as fuente:
            audio = reconocedor.record(fuente)
            texto = reconocedor.recognize_google(audio, language="es-ES")
            return texto
            
    except sr.UnknownValueError:
        return "No se pudo entender el audio (calidad baja o silencio)"
    except sr.RequestError:
        return "Error de conexión con el servicio de reconocimiento"
    except Exception as e:
        return f"Error en conversión: {str(e)}"


def encriptar_base64(texto):
    """Convierte texto plano a Base64 (encriptación reversible simple)"""
    if not texto or texto.strip() == "":
        return ""
    return base64.b64encode(texto.encode('utf-8')).decode('utf-8')


def desencriptar_base64(texto_encriptado):
    """Convierte texto Base64 de vuelta a texto plano"""
    if not texto_encriptado or texto_encriptado.strip() == "":
        return ""
    try:
        texto_bytes = base64.b64decode(texto_encriptado.encode('utf-8'))
        return texto_bytes.decode('utf-8')
    except:
        return "Error: Texto en Base64 no válido"


# SECCIÓN 4: RUTAS Y CONTROLADORES PRINCIPALES

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal que maneja todas las interacciones:
    - GET: Muestra el formulario inicial
    - POST: Procesa subida, conversión, encriptación o limpieza
    """
    global estado_actual
    
    # Manejo de solicitudes POST (acciones del usuario)
    if request.method == 'POST':
        
        # Acción: Subir archivo de audio
        if 'audio_file' in request.files:
            archivo = request.files['audio_file']
            if archivo and es_audio_permitido(archivo.filename):
                # Guardar archivo en carpeta uploads
                filename = secure_filename(archivo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                archivo.save(filepath)
                
                # Actualizar estado con nueva información
                estado_actual['archivo'] = filename
                estado_actual['codigo_maquina'] = leer_codigo_maquina(filepath)
                estado_actual['texto'] = None
                estado_actual['texto_encriptado'] = None
                estado_actual['error'] = None
        
        # Acción: Convertir audio a texto
        elif 'convertir' in request.form and estado_actual['archivo']:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], estado_actual['archivo'])
            estado_actual['texto'] = convertir_audio_a_texto(filepath)
        
        # Acción: Encriptar texto resultante
        elif 'encriptar' in request.form and estado_actual['texto']:
            estado_actual['texto_encriptado'] = encriptar_base64(estado_actual['texto'])
        
        # Acción: Desencriptar texto
        elif 'desencriptar' in request.form and estado_actual['texto_encriptado']:
            estado_actual['texto'] = desencriptar_base64(estado_actual['texto_encriptado'])
            estado_actual['texto_encriptado'] = None
        
        # Acción: Limpiar todo y comenzar de nuevo
        elif 'limpiar' in request.form:
            # Limpiar estado
            estado_actual = {'archivo': None, 'codigo_maquina': None, 
                           'texto': None, 'texto_encriptado': None, 'error': None}
            # Eliminar archivos temporales
            for f in os.listdir(app.config['UPLOAD_FOLDER']):
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
                except:
                    pass
    
    # Renderizar la plantilla HTML con el estado actual
    return render_template('index.html', estado=estado_actual)

# SECCIÓN 5: INICIO DE LA APLICACIÓN


if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación.
    Inicia el servidor Flask en modo desarrollo.
    """
    print("=" * 60)
    print("FORMULARIO COMPUTACIONAL AUDIO-TEXTO")
    print("Desarrollado por: Leonardo Alexander Ventura Díaz")
    print("Matrícula: 2023-0548")
    print("=" * 60)
    print("Servidor iniciado en: http://localhost:5000")
    print("Formatos aceptados: MP3, WAV")
    print("Límite de audio: 60 segundos máximo")
    print("=" * 60)
    
    # Iniciar servidor con configuración de desarrollo
    app.run(debug=True, port=5000, host='0.0.0.0')