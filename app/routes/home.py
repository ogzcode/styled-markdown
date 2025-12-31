from flask import Blueprint, render_template, request, jsonify
import markdown
import os
from google import genai
from bs4 import BeautifulSoup
import cssutils
import logging

# Suppress cssutils warnings
cssutils.log.setLevel(logging.CRITICAL)

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


def apply_inline_styles(html_content, css_content):
    """Apply CSS styles as inline styles to HTML elements"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Parse CSS
    sheet = cssutils.parseString(css_content)
    
    # Create a dictionary to store styles for each selector
    styles_dict = {}
    
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            declarations = rule.style.cssText
            
            # Store styles for this selector
            if selector not in styles_dict:
                styles_dict[selector] = []
            
            # Parse individual declarations
            for prop in rule.style:
                styles_dict[selector].append(f"{prop.name}: {prop.value}")
    
    # Apply styles to matching elements
    for selector, style_list in styles_dict.items():
        try:
            # Find all matching elements
            elements = soup.select(selector)
            
            for element in elements:
                # Get existing style attribute
                existing_style = element.get('style', '')
                
                # Combine with new styles
                new_styles = '; '.join(style_list)
                
                if existing_style:
                    combined_style = f"{existing_style}; {new_styles}"
                else:
                    combined_style = new_styles
                
                element['style'] = combined_style
        except:
            # Skip invalid selectors
            continue
    
    # Wrap body content in a main div with body styles
    body_styles = []
    for selector in ['body', 'html']:
        if selector in styles_dict:
            body_styles.extend(styles_dict[selector])
    
    # Create wrapper div
    wrapper = soup.new_tag('div')
    wrapper['class'] = 'markdown-content'
    
    if body_styles:
        wrapper['style'] = '; '.join(body_styles)
    
    # Move all current content into wrapper
    contents = list(soup.children)
    for content in contents:
        wrapper.append(content.extract())
    
    soup.append(wrapper)
    
    return str(soup)


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

    # Apply inline styles
    styled_content = apply_inline_styles(html_output, css_content)

    # Wrap HTML without style tag
    styled_html = f""" {styled_content} """

    return jsonify({'html': styled_html})


@home_bp.route("/ai-css", methods=['POST'])
def ai_css():
    data = request.get_json()
    user_prompt = data.get('prompt', '')
    current_html = data.get('html', '')  # Get current HTML if provided

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

        # If HTML is provided, apply inline styles
        if current_html.strip():
            styled_html = apply_inline_styles(current_html, generated_css)
            return jsonify({'css': generated_css, 'html': styled_html})

        return jsonify({'css': generated_css})

    except FileNotFoundError:
        return jsonify({'error': 'CSS template not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
