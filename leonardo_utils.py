import os, json, time, requests, streamlit as st
from dotenv import load_dotenv

load_dotenv()
leonardo_api_key = os.getenv("LEONARDO_API_KEY")
LEONARDO_MODEL_ID = "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3"
IMAGE_WIDTH, IMAGE_HEIGHT, NUM_IMAGES = 512, 512, 8

def generate_leonardo_images(prompt: str) -> list[bytes] | None:
    """Schickt Prompt an Leonardo AI und liefert die Bild-Bytes zurück."""
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    hdr = {
        "Accept": "application/json",
        "Authorization": f"Bearer {leonardo_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "modelId": LEONARDO_MODEL_ID,
        "prompt": prompt[:1490],     # 1 500-Zeichen-Limit mit etwas Puffer
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "num_images": NUM_IMAGES,
    }

    resp = requests.post(url, headers=hdr, json=body, timeout=30)

    if resp.status_code != 200:
        # ↳ Fehler verständlich anzeigen und Ausstieg
        st.error(f"Leonardo API – HTTP {resp.status_code}\n{resp.text}")
        return None

    try:
        generation_id = resp.json()["sdGenerationJob"]["generationId"]
    except (KeyError, ValueError):
        st.error(f"Unerwartetes Antwortformat:\n{resp.text}")
        return None

    # -------- Poll-Loop --------
    status_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    bar = st.progress(0.0)
    status = "PENDING"

    while status not in ("COMPLETE", "FAILED"):
        time.sleep(3)
        stat_resp = requests.get(status_url, headers=hdr, timeout=15)
        stat = stat_resp.json().get("generations_by_pk", {})
        status = stat.get("status", "PENDING")
        bar.progress(0.7 if status == "IN_PROGRESS" else 0.3)

    if status == "FAILED":
        st.error("Leonardo meldet FAILED – siehe Dashboard für Details.")
        return None

    bar.progress(1.0)

    # -------- Bilder laden --------
    img_urls = [img["url"] for img in stat["generated_images"]]
    return [requests.get(u).content for u in img_urls]