from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime, timedelta
import os
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Performance optimizations
@app.after_request
def after_request(response):
    """Add performance and security headers"""
    # Cache static resources
    if request.endpoint == 'static':
        response.cache_control.max_age = 31536000  # 1 year
        response.cache_control.public = True
    else:
        # Cache dynamic content for a short time
        response.cache_control.max_age = 300  # 5 minutes
        response.cache_control.public = True
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Performance headers
    response.headers['Vary'] = 'Accept-Encoding'
    
    return response

def add_cache_headers(max_age=300):
    """Decorator to add cache headers to routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.cache_control.max_age = max_age
            response.cache_control.public = True
            return response
        return decorated_function
    return decorator

# SEO Configuration
SEO_CONFIG = {
    'site_name': 'GreenFarm - Premium Organic Solutions',
    'site_description': 'Leading provider of premium organic farming solutions, fertilizers, and sustainable agriculture products. Transform your farm with our eco-friendly, scientifically-proven organic solutions.',
    'site_url': 'https://greenfarm.com',
    'site_author': 'GreenFarm Team',
    'site_keywords': 'organic farming, organic fertilizer, sustainable agriculture, bio pesticides, soil conditioner, farm solutions, eco-friendly farming, organic products, agricultural supplies, green farming',
    'twitter_handle': '@greenfarm',
    'facebook_page': 'GreenFarmOfficial',
    'company_address': '123 Farm Road, Green Valley, CA 90210',
    'company_phone': '+1 (555) 123-4567',
    'company_email': 'info@greenfarm.com'
}

# SEO Helper Functions
def generate_page_seo(page_type, **kwargs):
    """Generate SEO metadata for different page types"""
    seo_data = {
        'site_name': SEO_CONFIG['site_name'],
        'site_url': SEO_CONFIG['site_url'],
        'twitter_handle': SEO_CONFIG['twitter_handle'],
        'facebook_page': SEO_CONFIG['facebook_page']
    }
    
    if page_type == 'home':
        seo_data.update({
            'title': 'GreenFarm - Premium Organic Farming Solutions | Sustainable Agriculture',
            'description': 'Transform your farm with GreenFarm\'s premium organic fertilizers, bio pesticides, and sustainable agriculture solutions. Trusted by farmers worldwide for eco-friendly, high-yield farming.',
            'keywords': 'organic farming, organic fertilizer, sustainable agriculture, bio pesticides, soil conditioner, eco-friendly farming, premium organic solutions',
            'canonical_url': SEO_CONFIG['site_url'],
            'og_image': f"{SEO_CONFIG['site_url']}/static/images/greenfarm-hero.jpg",
            'page_type': 'website'
        })
    elif page_type == 'about':
        seo_data.update({
            'title': 'About GreenFarm - Leading Organic Agriculture Company | Our Story',
            'description': 'Learn about GreenFarm\'s mission to revolutionize agriculture through sustainable, organic farming solutions. Discover our commitment to environmental stewardship and farmer success.',
            'keywords': 'about greenfarm, organic agriculture company, sustainable farming mission, agricultural innovation, environmental stewardship',
            'canonical_url': f"{SEO_CONFIG['site_url']}/about",
            'og_image': f"{SEO_CONFIG['site_url']}/static/images/greenfarm-about.jpg",
            'page_type': 'article'
        })
    elif page_type == 'products':
        seo_data.update({
            'title': 'Organic Farming Products | Premium Fertilizers & Bio Pesticides - GreenFarm',
            'description': 'Explore GreenFarm\'s comprehensive range of organic farming products including premium fertilizers, bio pesticides, and soil conditioners. Boost your crop yield naturally.',
            'keywords': 'organic farming products, organic fertilizers, bio pesticides, soil conditioners, natural farming solutions, agricultural products',
            'canonical_url': f"{SEO_CONFIG['site_url']}/products",
            'og_image': f"{SEO_CONFIG['site_url']}/static/images/greenfarm-products.jpg",
            'page_type': 'product'
        })
    elif page_type == 'contact':
        seo_data.update({
            'title': 'Contact GreenFarm - Get Expert Agricultural Consultation | Organic Farming Support',
            'description': 'Contact GreenFarm for expert agricultural consultation and support. Get personalized organic farming solutions and technical guidance from our experienced team.',
            'keywords': 'contact greenfarm, agricultural consultation, organic farming support, expert advice, farming guidance',
            'canonical_url': f"{SEO_CONFIG['site_url']}/contact",
            'og_image': f"{SEO_CONFIG['site_url']}/static/images/greenfarm-contact.jpg",
            'page_type': 'article'
        })
    elif page_type == 'product_detail':
        product = kwargs.get('product')
        if product:
            seo_data.update({
                'title': f"{product['name']} - Premium {product['category']} | GreenFarm Organic Solutions",
                'description': f"{product['description']} Premium {product['category'].lower()} from GreenFarm. {', '.join(product['features'])}. Order now for sustainable farming success.",
                'keywords': f"{product['name'].lower()}, {product['category'].lower()}, organic {product['category'].lower()}, {', '.join([f.lower() for f in product['features']])}",
                'canonical_url': f"{SEO_CONFIG['site_url']}/products/{product['id']}",
                'og_image': f"{SEO_CONFIG['site_url']}/static/images/products/{product['id']}.jpg",
                'page_type': 'product',
                'product_price': product['price'],
                'product_currency': 'USD'
            })
    
    return seo_data

def generate_structured_data(page_type, **kwargs):
    """Generate JSON-LD structured data for SEO"""
    base_organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "GreenFarm",
        "url": SEO_CONFIG['site_url'],
        "logo": f"{SEO_CONFIG['site_url']}/static/images/greenfarm-logo.png",
        "description": SEO_CONFIG['site_description'],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "123 Farm Road",
            "addressLocality": "Green Valley",
            "addressRegion": "CA",
            "postalCode": "90210",
            "addressCountry": "US"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": SEO_CONFIG['company_phone'],
            "contactType": "customer service",
            "email": SEO_CONFIG['company_email']
        },
        "sameAs": [
            f"https://twitter.com/{SEO_CONFIG['twitter_handle']}",
            f"https://facebook.com/{SEO_CONFIG['facebook_page']}"
        ]
    }
    
    if page_type == 'home':
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SEO_CONFIG['site_name'],
            "url": SEO_CONFIG['site_url'],
            "description": SEO_CONFIG['site_description'],
            "publisher": base_organization,
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{SEO_CONFIG['site_url']}/search?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        }
    elif page_type == 'products':
        products = kwargs.get('products', [])
        products_data = []
        for product in products:
            products_data.append({
                "@type": "Product",
                "name": product['name'],
                "description": product['description'],
                "category": product['category'],
                "offers": {
                    "@type": "Offer",
                    "price": product['price'],
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "seller": base_organization
                }
            })
        
        return {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": products_data
        }
    elif page_type == 'product_detail':
        product = kwargs.get('product')
        if product:
            return {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": product['name'],
                "description": product['description'],
                "category": product['category'],
                "brand": {
                    "@type": "Brand",
                    "name": "GreenFarm"
                },
                "offers": {
                    "@type": "Offer",
                    "price": product['price'],
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "seller": base_organization
                }
            }
    elif page_type == 'contact':
        return {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "mainEntity": base_organization
        }
    
    return base_organization

# Make SEO functions available in templates
@app.context_processor
def inject_seo():
    return {
        'generate_page_seo': generate_page_seo,
        'generate_structured_data': generate_structured_data,
        'seo_config': SEO_CONFIG
    }
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[Length(min=10, max=15)])
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('quote', 'Request Quote'),
        ('support', 'Technical Support'),
        ('partnership', 'Partnership Opportunity')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

@app.route('/')
@add_cache_headers(600)  # Cache homepage for 10 minutes
def home():
    seo_data = generate_page_seo('home')
    structured_data = generate_structured_data('home')
    return render_template('index.html', seo=seo_data, structured_data=json.dumps(structured_data))

@app.route('/about')
def about():
    seo_data = generate_page_seo('about')
    structured_data = generate_structured_data('about')
    return render_template('about.html', seo=seo_data, structured_data=json.dumps(structured_data))

@app.route('/products')
def products():
    # Sample product data - in a real app, this would come from a database
    products = [
        {
            'id': 1,
            'name': 'Organic Fertilizer',
            'description': 'Premium blend of natural nutrients to enhance soil fertility and plant growth.',
            'price': 49.99,
            'category': 'Fertilizers',
            'features': ['100% Organic', 'Slow Release', 'NPK Balanced']
        },
        {
            'id': 2,
            'name': 'Soil Conditioner',
            'description': 'Advanced formula to improve soil structure and water retention capacity.',
            'price': 39.99,
            'category': 'Soil Care',
            'features': ['Improves Drainage', 'Enhances Structure', 'Organic Matter']
        },
        {
            'id': 3,
            'name': 'Bio Pesticide',
            'description': 'Natural pest control solution that\'s safe for crops and environment.',
            'price': 59.99,
            'category': 'Pest Control',
            'features': ['Chemical-Free', 'Safe for Beneficial Insects', 'Fast Acting']
        }
    ]
    seo_data = generate_page_seo('products')
    structured_data = generate_structured_data('products', products=products)
    return render_template('products.html', products=products, seo=seo_data, structured_data=json.dumps(structured_data))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # In a real application, you would process the form data here
        # (save to database, send email, etc.)
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    seo_data = generate_page_seo('contact')
    structured_data = generate_structured_data('contact')
    return render_template('contact.html', form=form, seo=seo_data, structured_data=json.dumps(structured_data))

@app.route('/privacy-policy')
def privacy_policy():
    seo_data = {
        'title': 'Privacy Policy - GreenFarm | Data Protection & Privacy',
        'description': 'Read GreenFarm\'s privacy policy to understand how we protect your personal information and data. Learn about our commitment to your privacy and security.',
        'keywords': 'privacy policy, data protection, greenfarm privacy, personal information security',
        'canonical_url': f"{SEO_CONFIG['site_url']}/privacy-policy"
    }
    return render_template('privacy_policy.html', seo=seo_data)

@app.route('/terms-of-service')
def terms_of_service():
    seo_data = {
        'title': 'Terms of Service - GreenFarm | User Agreement & Conditions',
        'description': 'Read GreenFarm\'s terms of service and user agreement. Understand the terms and conditions for using our organic farming products and services.',
        'keywords': 'terms of service, user agreement, greenfarm terms, service conditions',
        'canonical_url': f"{SEO_CONFIG['site_url']}/terms-of-service"
    }
    return render_template('terms_of_service.html', seo=seo_data)

@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap.xml"""
    pages = []
    
    # Static pages
    static_pages = [
        {'url': url_for('home', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'changefreq': 'weekly', 'priority': '1.0'},
        {'url': url_for('about', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'changefreq': 'monthly', 'priority': '0.8'},
        {'url': url_for('products', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'changefreq': 'weekly', 'priority': '0.9'},
        {'url': url_for('contact', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'changefreq': 'monthly', 'priority': '0.7'},
        {'url': url_for('privacy_policy', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'changefreq': 'yearly', 'priority': '0.3'},
        {'url': url_for('terms_of_service', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'changefreq': 'yearly', 'priority': '0.3'},
    ]
    
    pages.extend(static_pages)
    
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    for page in pages:
        sitemap_xml += f'''  <url>
    <loc>{page['url']}</loc>
    <lastmod>{page['lastmod']}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>
'''
    
    sitemap_xml += '</urlset>'
    
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def robots():
    """Generate robots.txt"""
    robots_txt = '''User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /*.json$

Sitemap: {}/sitemap.xml

# Crawl-delay for polite crawling
Crawl-delay: 1

# Allow all major search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /
'''.format(SEO_CONFIG['site_url'])
    
    response = make_response(robots_txt)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/api/schema/<page_type>')
@add_cache_headers(3600)  # Cache schema for 1 hour
def api_schema(page_type):
    """API endpoint for JSON-LD structured data"""
    if page_type == 'organization':
        schema_data = generate_structured_data('home')
    elif page_type == 'products':
        products = [
            {
                'id': 1,
                'name': 'Organic Fertilizer',
                'description': 'Premium blend of natural nutrients to enhance soil fertility and plant growth.',
                'price': 49.99,
                'category': 'Fertilizers',
                'features': ['100% Organic', 'Slow Release', 'NPK Balanced']
            },
            {
                'id': 2,
                'name': 'Soil Conditioner',
                'description': 'Advanced formula to improve soil structure and water retention capacity.',
                'price': 39.99,
                'category': 'Soil Care',
                'features': ['Improves Drainage', 'Enhances Structure', 'Organic Matter']
            },
            {
                'id': 3,
                'name': 'Bio Pesticide',
                'description': 'Natural pest control solution that\'s safe for crops and environment.',
                'price': 59.99,
                'category': 'Pest Control',
                'features': ['Chemical-Free', 'Safe for Beneficial Insects', 'Fast Acting']
            }
        ]
        schema_data = generate_structured_data('products', products=products)
    else:
        return jsonify({'error': 'Invalid schema type'}), 404
    
    response = jsonify(schema_data)
    response.headers['Content-Type'] = 'application/ld+json'
    return response

@app.route('/api/quote', methods=['POST'])
def api_quote():
    """API endpoint for quote requests"""
    try:
        data = request.get_json()
        # In a real application, you would process the quote request here
        # (save to database, send email notification, etc.)
        
        # Simulate processing
        response = {
            'success': True,
            'message': 'Quote request received successfully! We\'ll contact you within 24 hours.',
            'quote_id': 'QT-2025-001'
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request. Please try again.'
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)