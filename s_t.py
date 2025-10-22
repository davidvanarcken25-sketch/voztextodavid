import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from gtts import gTTS
from googletrans import Translator
from PIL import Image
import glob
import time

# ==========================
# CONFIGURACIÓN DE PÁGINA
# ==========================
st.set_page_config(page_title="CYRA - Cyber Translator 2077", page_icon="🤖", layout="centered")

# ==========================
# ESTILOS FUTURISTAS
# ==========================
st.markdown("""
    <style>
    body {
        background-color: #0a0a0f;
        color: #E0E0E0;
        font-family: 'Courier New', monospace;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f1f 0%, #000000 100%);
    }
    .title {
        font-size: 45px;
        text-align: center;
        color: #00FFFF;
        font-weight: bold;
        text-shadow: 0px 0px 20px #00FFFF;
        letter-spacing: 2px;
    }
    .subtitle {
        text-align: center;
        color: #A0A0A0;
        font-size: 18px;
    }
    .neon-box {
        background: rgba(0,255,255,0.1);
        border: 2px solid #00FFFF;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0px 0px 20px #00FFFF50;
    }
    .stButton>button {
        background-color: #00FFFF;
        color: #000;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF00FF;
        color: white;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #FF00FF;
    }
    .footer {
        text-align: center;
        color: #555;
        font-size: 12px;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# INTERFAZ PRINCIPAL
# ==========================
st.markdown("<div class='title'>CYRA - Cyber Translator 2077 🤖</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Traducción por voz en tiempo real con inteligencia sintética</div>", unsafe_allow_html=True)

try:
    image = Image.open('cyra_avatar.png')
    st.image(image, width=320, caption="CYRA - Neural Linguistic System v2.1")
except:
    st.warning("⚠️ Añade una imagen llamada 'cyra_avatar.jpg' para personalizar la interfaz visual del asistente.")

st.divider()

st.markdown("<div class='neon-box'><b>🎙️ Activación de micrófono:</b><br>Habla y CYRA analizará tu voz en tiempo real.</div>", unsafe_allow_html=True)

# ==========================
# BOTÓN DE ESCUCHA
# ==========================
stt_button = Button(label="🎧 Activar Escucha", width=280, button_type="primary")
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# ==========================
# PROCESAMIENTO Y TRADUCCIÓN
# ==========================
if result:
    if "GET_TEXT" in result:
        user_text = result.get("GET_TEXT")
        st.markdown(f"<div class='neon-box'>🗣️ <b>Entrada detectada:</b> {user_text}</div>", unsafe_allow_html=True)

        # Idiomas
        translator = Translator()
        st.divider()
        st.markdown("<div class='subtitle'>🌐 Configuración de Traducción</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            input_lang = st.selectbox("Idioma original", ["Español", "Inglés", "Japonés", "Coreano", "Francés"])
        with col2:
            output_lang = st.selectbox("Idioma destino", ["Inglés", "Español", "Japonés", "Coreano", "Francés"])

        lang_map = {
            "Español": "es",
            "Inglés": "en",
            "Japonés": "ja",
            "Coreano": "ko",
            "Francés": "fr"
        }

        in_lang_code = lang_map[input_lang]
        out_lang_code = lang_map[output_lang]

        # Conversión
        def translate_and_speak(text):
            translation = translator.translate(text, src=in_lang_code, dest=out_lang_code)
            tts = gTTS(translation.text, lang=out_lang_code)
            os.makedirs("temp", exist_ok=True)
            file_path = f"temp/cyra_{int(time.time())}.mp3"
            tts.save(file_path)
            return translation.text, file_path

        if st.button("🚀 Ejecutar Traducción Neural"):
            with st.spinner("Procesando datos neuronales... ⚡"):
                translated_text, audio_path = translate_and_speak(user_text)
                st.success("✅ Traducción completa.")
                st.markdown(f"<div class='neon-box'>🧠 <b>Traducción:</b><br>{translated_text}</div>", unsafe_allow_html=True)

                audio_file = open(audio_path, "rb")
                st.audio(audio_file.read(), format="audio/mp3")

# ==========================
# PIE DE PÁGINA
# ==========================
st.markdown("<div class='footer'>CYRA Neural Systems © 2077 — Proyecto experimental de traducción por voz</div>", unsafe_allow_html=True)


    


