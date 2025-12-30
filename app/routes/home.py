from flask import Blueprint, render_template, request, jsonify
import markdown
import os
from google import genai

home_bp = Blueprint('home', __name__)

# Initialize Gemini client
genai_client = genai.Client()


def read_css_file(theme='light'):
    """Read CSS file based on theme selection"""
    css_file = f'blog-{theme}.css'
    css_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'static/css', css_file)

    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''


@home_bp.route("/")
def home():
    return render_template("base.html")


@home_bp.route("/convert", methods=['POST'])
def convert():
    data = request.get_json()
    markdown_text = data.get('markdown', '')
    theme = data.get('theme', 'light')

    # Convert markdown to HTML
    html_output = markdown.markdown(
        markdown_text,
        extensions=['extra', 'codehilite', 'fenced_code', 'tables']
    )

    # Read CSS based on theme
    css_content = read_css_file(theme)

    # Wrap HTML with style tag
    styled_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{css_content}
    </style>
</head>
<body>
{html_output}
</body>
</html>"""

    return jsonify({'html': styled_html})


@home_bp.route("/ai-css", methods=['POST'])
def ai_css():
    data = request.get_json()
    user_prompt = data.get('prompt', '')

    if not user_prompt.strip():
        return jsonify({'error': 'Prompt cannot be empty'}), 400

    # Read the CSS prompt template
    template_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'static', 'css-prompt-template.txt')

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Replace {user_prompt} with actual user input
        full_prompt = template.replace('{user_prompt}', user_prompt)

        # Generate CSS using Gemini
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=full_prompt,
        )

        generated_css = response.text.strip()

        # Clean up if model returns markdown code blocks
        if generated_css.startswith('```css'):
            generated_css = generated_css[6:]
        if generated_css.startswith('```'):
            generated_css = generated_css[3:]
        if generated_css.endswith('```'):
            generated_css = generated_css[:-3]

        generated_css = generated_css.strip()

        return jsonify({'css': generated_css})

    except FileNotFoundError:
        return jsonify({'error': 'CSS template not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
