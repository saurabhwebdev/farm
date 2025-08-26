from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Contact Form
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
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
    return render_template('products.html', products=products)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # In a real application, you would process the form data here
        # (save to database, send email, etc.)
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

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