# Farm Website

A simple Flask web application for a farm business.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure

```
farm/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   └── about.html     # About page
├── static/            # Static files
│   └── css/
│       └── style.css  # CSS styles
└── README.md          # This file
```

## Features

- Home page with farm information
- About page with farm story
- Responsive design
- Clean, modern styling

## Development

The application runs in debug mode by default, so changes to the code will automatically reload the server.