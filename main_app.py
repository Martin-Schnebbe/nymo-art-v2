import os
import io
from PIL import Image
import streamlit as st

from file_utils import create_timestamp_folder, save_text, save_image
from openai_utils import get_initial_prompt, get_improved_prompt
from leonardo_utils import generate_leonardo_images


def main() -> None:
    st.title("🎨 Art Prompt Lab")

    # Work-Dir vorbereiten
    os.makedirs("runs", exist_ok=True)

    # ---------- Eingabe ----------
    style_text = st.text_area(
        label="Style / Idea",
        placeholder="Describe the art style or concept…",
        height=100,
        help="Describe the art style or concept you want to generate"
    )
    uploaded_image = st.file_uploader(
        label="Reference image (optional)",
        type=["png", "jpg", "jpeg"],
        help="Upload a reference image to guide the generation"
    )

    # ---------- Aktion ----------
    if st.button("Generate"):
        if not style_text.strip():
            st.error("Please enter a style or idea description")
            st.stop()

        with st.spinner("Processing…"):
            folder_path = create_timestamp_folder()

            # Eingabe sichern
            save_text(folder_path, "style.txt", style_text)
            reference_image_data = None
            if uploaded_image is not None:
                reference_image_data = uploaded_image.getvalue()
                save_image(folder_path, "ref.png", reference_image_data)

            # Prompt v1 erzeugen
            v1_prompt = get_initial_prompt(style_text, reference_image_data)
            save_text(folder_path, "v1_prompt.txt", v1_prompt)

            # Bilder generieren
            images = generate_leonardo_images(v1_prompt) or []
            for i, img_data in enumerate(images):
                save_image(folder_path, f"img_{i+1}.png", img_data)

            # Prompt v2 erzeugen
            v2_prompt = get_improved_prompt(v1_prompt, images)
            save_text(folder_path, "v2_prompt.txt", v2_prompt)

        # ---------- Ausgabe ----------
        st.subheader("Initial Prompt (v1)")
        st.text_area(
            label="Initial prompt text",
            value=v1_prompt,
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )

        st.subheader("Generated Images")
        cols = st.columns(4)
        for i, img_data in enumerate(images):
            img = Image.open(io.BytesIO(img_data))
            cols[i % 4].image(
                img,
                caption=f"Image {i+1}",
                use_container_width=True
            )

        st.subheader("Improved Prompt (v2)")
        st.text_area(
            label="Improved prompt text",
            value=v2_prompt,
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )

        st.success(f"All files saved in folder: {folder_path}")


if __name__ == "__main__":
    main()