# Template Structure

This directory contains the modularized template components for the application.

## Structure

```
templates/
├── base.html                    # Base template with common HTML structure
├── index.html                   # Main page using components
├── greyscale_index.html         # Original template (backup: greyscale_index_backup.html)
└── components/
    ├── navbar.html              # Navigation bar component
    ├── masthead.html            # Hero/header section component
    ├── about.html               # About section component
    ├── projects.html            # Projects/travel section component
    ├── contact.html             # Contact section component
    ├── contact_card.html        # Individual contact card component
    ├── newsletter.html          # Newsletter signup form component
    └── footer.html              # Footer component
```

## Usage

### Base Template
The `base.html` template provides the common HTML structure including:
- HTML document structure
- CSS and JavaScript includes
- Template blocks for customization

### Components
Each component is self-contained and can be included in any template using:
```jinja2
{% include 'components/component_name.html' %}
```

### Customization
Components support customization through template blocks:
- `{% block block_name %}default content{% endblock %}`

### Example Usage
```jinja2
{% extends "base.html" %}

{% block title %}Custom Page Title{% endblock %}

{% block navbar %}
{% include 'components/navbar.html' %}
{% endblock %}

{% block content %}
{% include 'components/masthead.html' %}
{% include 'components/about.html' %}
{% endblock %}
```

## Benefits

1. **Reusability**: Components can be used across multiple pages
2. **Maintainability**: Changes to components only need to be made in one place
3. **Flexibility**: Easy to create different page layouts by combining components
4. **Content Management**: Dynamic content can be passed to components via template variables
5. **Testing**: Individual components can be tested in isolation
