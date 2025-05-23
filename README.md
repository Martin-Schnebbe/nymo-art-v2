# Art Prompt Lab MVP

A minimal Streamlit tool that transforms a style description and optional reference image into detailed art prompts and generated images using GPT-4 Vision and Leonardo AI.

## Quick Start

```bash
git clone <repo-url>
cd art-prompt-lab
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add OPENAI_API_KEY and LEONARDO_API_KEY
streamlit run app.py
```

## Features

1. **Input Interface**: Enter a style/idea description and optionally upload a reference image.
2. **Initial Prompt Generation**: Uses GPT-4 Vision to create a detailed art prompt based on your inputs.
3. **Image Generation**: Creates 8 images using Leonardo AI based on the generated prompt.
4. **Improved Prompt**: Analyses the generated images and creates an improved, more focused prompt for future use.
5. **File Storage**: All inputs, prompts, and generated images are saved in timestamped folders.

## Workflow

1. Enter your style/idea description
2. Optionally upload a reference image
3. Click "Generate"
4. Wait for the process to complete
5. View the initial prompt, generated images, and improved prompt
6. Find all files saved in the `runs/<timestamp>` folder

## API Keys

You'll need:
- OpenAI API key (with access to GPT-4 Vision)
- Leonardo AI API key

Add these to your `.env` file:
```
OPENAI_API_KEY=your_openai_key_here
LEONARDO_API_KEY=your_leonardo_key_here
```
