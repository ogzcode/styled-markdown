from flask import Blueprint, render_template, request, jsonify
import markdown
import os

home_bp = Blueprint('home', __name__)

def read_css_file(theme='light'):
    """Read CSS file based on theme selection"""
    css_file = f'blog-{theme}.css'
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', css_file)
    
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