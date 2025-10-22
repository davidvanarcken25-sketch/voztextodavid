import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

# ==========================
# CONFIGURACIÓN DE PÁGINA
# ==========================
st.set_page_config(page_title="Emma - Asistente Traductora", page_icon="🎧", layout="centered")

# ==========================
# ESTILOS PERSONALIZADOS
# ==========================
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            color: #6C63FF;
            text-align: center;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #4B4B4B;
        }
        .note-box {
            background-color: #EDEBFF;
            padding: 15px;
            border-radius: 12px;
            border-left: 5px solid #6C63FF;
            margin-top: 20px;
            color: #000000;
            font-size: 17px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #777;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================
# ENCABEZADO E IMAGEN PRINCIPAL
# ==========================
st.markdown("<div class='title'>🎓 EMMA - Tu Asistente Traductora</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Habla y deja que Emma traduzca tus palabras al instante 🌍</div>", unsafe_allow_html=True)

image = Image.open('OIG7.jpg')
st.image(image, width=280, caption="Emma, tu traductora por voz inteligente 🎙️")

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.markdown("## 🌐 Panel de Traducción")
    st.write("Presiona el botón y habla lo que deseas traducir. Luego selecciona los idiomas de entrada y salida para que Emma te ayude.")
    st.info("Consejo: asegúrate de tener el micrófono habilitado en tu navegador 🎤")

st.divider()
st.markdown("### 🎤 Habla con Emma")
st.write("Haz clic en el botón y empieza a hablar. Emma escuchará lo que digas y lo traducirá automáticamente 🪶")

# ==========================
# BOTÓN DE RECONOCIMIENTO DE VOZ
# ==========================
stt_button = Button(label="🎙️ Escuchar con Emma", width=300, height=50, button_type="success")

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

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

# ==========================
# CAPTURAR VOZ
# ==========================
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# ==========================
# PROCESAR Y TRADUCIR TEXTO
# ==========================
if result:
    if "GET_TEXT" in result:
        user_text = result.get("GET_TEXT")
        st.markdown(f"<div class='note-box'>🗒️ <b>Emma escuchó:</b><br>{user_text}</div>", unsafe_allow_html=True)

    # Crear carpeta temporal
    os.makedirs("temp", exist_ok=True)

    translator = Translator()

    st.divider()
    st.markdown("### 🌍 Configuración de Traducción")

    # Idioma de entrada
    in_lang = st.selectbox(
        "Selecciona el idioma de entrada:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"

    # Idioma de salida
    out_lang = st.selectbox(
        "Selecciona el idioma de salida:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"

    # Acento
    english_accent = st.selectbox(
        "Selecciona el acento para la voz:",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canadá",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )

    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canadá":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"

    # Función de traducción
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    display_output_text = st.checkbox("📘 Mostrar texto traducido")

    if st.button("✨ Traducir con Emma"):
        result_file, output_text = text_to_speech(input_language, output_language, user_text, tld)
        audio_file = open(f"temp/{result_file}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## 🔊 Traducción de Emma:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## 📝 Texto traducido:")
            st.write(output_text)

    # Limpieza de archivos temporales
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)

st.markdown("<div class='footer'>Hecho con 💜 por Emma — Tu asistente traductora personal</div>", unsafe_allow_html=True)

    


