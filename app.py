import streamlit as st
from google import genai

# Configuración básica de la página
st.set_page_config(page_title="¡Aprende Inglés Natural!", page_icon="🧮")

st.title("🧮 Aprende Inglés Natural")
st.caption("Escribe tu frase para obtener directamente la versión en inglés natural.")

# 1. Obtenemos la API Key automáticamente desde los Secrets de Streamlit
# (Esto reemplaza por completo el campo de texto de la barra lateral)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
   st.error("No se encontró la API Key en los Secrets de Streamlit. Por favor, revísala en la configuración.")
else:
    try:
        # Inicializamos el cliente oficial de Google GenAI con la llave segura
        client = genai.Client(api_key=api_key)

        if "corrected_text" not in st.session_state:
            st.session_state.corrected_text = ""

        def clear_screen():
            st.session_state.corrected_text = ""

        # 1. Campo de entrada del usuario
        user_input = st.text_input(
            "1. Escribe tu frase en inglés (tu intento o calco):",
            placeholder="Ejemplo: I have 25 years old",
            key="user_input_key"
        )

        if st.button("Corregir 🚀"):
            if user_input.strip():
                # Pedido ultrasimple: solo la versión natural
                prompt = f"Corrige el siguiente texto en inglés para que suene 100% natural. Responde ÚNICAMENTE con la versión corregida en inglés, sin explicaciones ni introducciones: '{user_input}'"

                try:
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=prompt,
                    )
                    st.session_state.corrected_text = response.text.strip()
                except Exception as e:
                    st.error(f"Ocurrió un error con Gemini: {e}")
            else:
                st.warning("Por favor ingresa una frase antes de hacer clic en corregir.")

        # 2. Área de resultado
        if st.session_state.corrected_text:
            st.markdown("---")
            st.subheader("2. Versión Natural:")
            st.code(st.session_state.corrected_text, language="text")

            # 3. Práctica de reescritura
            st.markdown("---")
            st.subheader("3. Practica reescribiendo la frase natural:")
            practice_input = st.text_input(
                "Teclea aquí la versión correcta para fijarla en tu memoria:",
                key="practice_input_key"
            )
            if practice_input:
                if practice_input.strip() == st.session_state.corrected_text.strip():
                    st.success("✅ ¡Excelente! Frase memorizada correctamente.")
                else:
                    st.warning("⚠️ Hay alguna diferencia. Revisa mayúsculas o signos de puntuación.")

            st.button("Limpiar y nueva frase 🧹", on_click=clear_screen)

    except Exception as e:
        st.error(f"Error al configurar la API Key: {e}")
else:
    st.info("👈 Por favor, ingresa tu API Key en la barra lateral para comenzar.")
