import os, base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _img2url(data: bytes) -> str:
    b64 = base64.b64encode(data).decode()
    return f"data:image/jpeg;base64,{b64}"

def get_initial_prompt(style_text: str, reference_image: bytes | None = None) -> str:
    content = [{"type": "input_text", "text": style_text}]
    if reference_image:
        content.append({"type": "input_image", "image_url": _img2url(reference_image)})

    rsp = client.responses.create(
        model="gpt-4.1",
        instructions=(
            "You are an art historian & prompt engineer. "
            "Write a rich, poetic prompt (≈50–100 words) that transforms the supplied text "
            "(and image, if any) into a concept for a single illustrative artwork. "
            "Use evocative art vocabulary; avoid camera or renderer jargon."
        ),
        input=[{"role": "user", "content": content}],
        temperature=1,
        max_output_tokens=2048,
    )
    return rsp.output_text

def get_improved_prompt(initial_prompt: str, images: list[bytes]) -> str:
    content = [{
        "type": "input_text",
        "text": (
            "Initial prompt:\n" + initial_prompt +
            "\n\nAnalyse what worked or failed. "
            "Rewrite the prompt in ≤ 180 words so that the next batch will be more coherent, "
            "more impressive, and stylistically consistent."
        )
    }]
    content += [
        {"type": "input_image", "image_url": _img2url(img)} for img in images
    ]

    rsp = client.responses.create(
        model="gpt-4.1",
        instructions=(
            "You are an art historian & prompt engineer. Analyse the images generated "
            "from the initial prompt and provide an improved prompt."
        ),
        input=[{"role": "user", "content": content}],
        temperature=1,
        max_output_tokens=2048,
    )
    return rsp.output_text