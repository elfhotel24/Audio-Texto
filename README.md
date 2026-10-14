# 🎙️ Formulario Computacional Audio-Texto

Aplicación web desarrollada en **Python con Flask** que permite cargar un archivo de audio, convertirlo a código de máquina hexadecimal, transcribirlo a texto y aplicar encriptación/desencriptación en Base64.

**Proyecto académico** — Estudiante: **Leonardo Alexander Ventura Díaz** — Matrícula: **2023-0548**

---

## 📋 Descripción

Este proyecto implementa un flujo completo de procesamiento de audio en el navegador mediante un servidor Flask:

1. **Cargar archivo de audio** (máx. 60 segundos).
2. **Generar código de máquina** en hexadecimal a partir del audio.
3. **Convertir a texto** (transcripción mediante reconocimiento de voz).
4. **Encriptar el texto** resultante en Base64.
5. **Desencriptar** para recuperar el texto original.

---

## 🛠️ Tecnologías utilizadas

| Componente          | Tecnología          |
|---------------------|---------------------|
| Lenguaje            | Python 3.x          |
| Framework Web       | Flask               |
| Reconocimiento voz  | SpeechRecognition   |
| Procesamiento audio | Librosa             |
| Frontend            | HTML + Jinja2       |

---

## 📁 Estructura del proyecto
InteligenciaAT/
├── app.py # Servidor Flask principal
├── templates/
│ └── index.html # Interfaz del formulario
├── static/ # CSS, JS, imágenes
├── uploads/ # Audios temporales (ignorado por Git)
├── requirements.txt # Dependencias del proyecto
├── .gitignore # Archivos ignorados por Git
└── README.md # Este archivo

text

---

## 🚀 Instalación y ejecución

### Requisitos previos

- Python 3.8 o superior
- pip
- **FFmpeg** instalado en el sistema (necesario para `SpeechRecognition` y `librosa`)
  - Windows: descargar de [ffmpeg.org](https://ffmpeg.org/download.html) y agregar al PATH
  - Linux: `sudo apt install ffmpeg`
  - Mac: `brew install ffmpeg`

### Pasos

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/elfhotel24/Audio-Texto.git
   cd Audio-Texto
Crea y activa un entorno virtual:

bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
Instala las dependencias:

bash
pip install -r requirements.txt
Ejecuta la aplicación:

bash
python app.py
Abre en el navegador:

text
http://127.0.0.1:5000
⚙️ Funcionalidades
✅ Cargar audio — Sube un archivo de hasta 60 segundos de duración.

✅ Código de máquina — Conversión del audio a representación hexadecimal.

✅ Transcripción — Conversión de audio a texto con SpeechRecognition.

✅ Encriptación Base64 — Cifrado simple del texto resultante.

✅ Desencriptación — Recuperación del texto original.

✅ Limpiar todo — Reinicia el formulario y el estado.

⚠️ Limitaciones
El archivo de audio no debe superar los 60 segundos.

El reconocimiento de voz funciona mejor con audio claro y sin ruido de fondo.

Formatos soportados: WAV, MP3, M4A, OGG, FLAC (según FFmpeg).

👤 Autor
Leonardo Alexander Ventura Díaz

Matrícula: 2023-0548

GitHub: @elfhotel24

📚 Contexto académico
Proyecto desarrollado como parte del curso de Inteligencia Artificial — Formulario Computacional Audio-Texto.

⭐ Si este proyecto te resultó útil, considera darle una estrella en GitHub.

text

---

### 💡 Nota especial para este proyecto

Como usa **archivos de audio**, es muy importante que verifiques que **NO** se suban audios de prueba grandes al repositorio. El `.gitignore` ya los excluye, pero revisa con `git status` antes del commit.

Avísame cuando termines el push. 🚀
