import streamlit as st
import cv2
import requests
import tempfile
import time

# Page configuration
st.set_page_config(page_title="YOLOv5 Waste Classifier", layout="wide")

# Titre et sous-titre de l'application
st.title("🌟 YOLOv5 Waste Classifier 🌟")
st.markdown("### Analysez des objets en direct via la caméra ou téléchargez une image pour une classification.")

# Sélection de mode via onglets
tab_live, tab_upload = st.tabs(["🎥 Analyse en direct", "📁 Téléchargement d'image"])

# ======================
# Onglet 1: Analyse en direct
# ======================
with tab_live:
    st.markdown("### 🎥 Analyse en direct")
    col1, col2 = st.columns(2)
    
    # Colonne 1: Boutons d'activation et désactivation
    with col1:
        start_button = st.button("▶️ Activer la caméra")
        stop_button = st.button("⏹️ Désactiver la caméra")

    # Colonne 2: Placeholder pour la vidéo
    with col2:
        video_placeholder = st.empty()
        status_placeholder = st.empty()

    # Variable pour contrôler l'état de la caméra
    camera_active = False

    # Capture de la caméra
    if start_button:
        camera_active = True
        cap = cv2.VideoCapture(1)  # Utilise la caméra virtuelle (OBS)

        if not cap.isOpened():
            status_placeholder.error("🚫 Impossible d'ouvrir la caméra.")
            camera_active = False
        else:
            status_placeholder.success("✅ Caméra activée. Analyse en cours...")

            while camera_active:
                ret, frame = cap.read()
                if not ret:
                    status_placeholder.error("🚫 Erreur lors de la capture des frames.")
                    break

                # Sauvegarder temporairement la frame
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
                    cv2.imwrite(temp_img.name, frame)

                    # Envoyer l'image au backend FastAPI
                    with open(temp_img.name, "rb") as img_file:
                        response = requests.post("http://127.0.0.1:8000/predict", files={"file": img_file})

                        if response.status_code == 200:
                            # Lire et afficher l'image annotée
                            annotated_img = response.content
                            video_placeholder.image(annotated_img, channels="BGR", use_column_width=True)
                        else:
                            status_placeholder.error("🚫 Erreur de l'API lors du traitement.")

                # Vérifier si le bouton stop est cliqué
                if stop_button:
                    camera_active = False
                    status_placeholder.warning("⏹️ Caméra désactivée.")
                    cap.release()
                    break

                time.sleep(0.1)  # Pour réduire la charge CPU

# ======================
# Onglet 2: Téléchargement d'image
# ======================
with tab_upload:
    st.markdown("### 📁 Téléchargement d'une image")
    uploaded_file = st.file_uploader("Téléchargez une image au format JPG, JPEG ou PNG", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.info("🔄 Traitement de l'image...")
        
        # Sauvegarder temporairement l'image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
            temp_img.write(uploaded_file.read())
            temp_img.flush()

            # Envoyer l'image au backend FastAPI
            with open(temp_img.name, "rb") as img_file:
                response = requests.post("http://127.0.0.1:8000/predict", files={"file": img_file})

                if response.status_code == 200:
                    # Lire l'image annotée et afficher
                    annotated_img = response.content
                    st.image(annotated_img, caption="🖼️ Image Annotée", use_column_width=True)
                else:
                    st.error("🚫 Erreur lors de la communication avec l'API.")