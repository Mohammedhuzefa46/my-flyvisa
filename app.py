import os
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError  # Importing the email validator

# Load environment variables (ensure you have a .env file with the required details)
load_dotenv()

app = Flask(_name_)

# Configure the app with database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'  # SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')  # Secure key for flashing messages

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')  # Your email
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')  # Your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')  # Default sender email

# Initialize database and mail
db = SQLAlchemy(app)
mail = Mail(app)

# Email Model to store email addresses in the database
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(120), nullable=False)  # Remove unique=True here

    def _repr_(self):
        return f'<Email {self.email_address}>'


# Create the database (if it doesn't exist)
with app.app_context():
    db.create_all()

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Main page with forms

# Route for the contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    email = request.form.get('email')
    print(url_for('contact'))

    if email:
        # Validate email format
        try:
            valid = validate_email(email)  # This checks if the email format is valid
        except EmailNotValidError as e:
            flash(f"Invalid email address: {str(e)}", 'danger')
            return redirect(url_for('index'))

        # Store the email in the database (allowing duplicates)
        new_email = Email(email_address=email)
        try:
            db.session.add(new_email)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error while saving your email: {str(e)}', 'danger')
            return redirect(url_for('index'))

        # Send a confirmation email to the customer
        msg = Message('Thank you for reaching out!',
                      recipients=[email])
        msg.body = 'Thank you for contacting us. We will get back to you soon.'
        try:
            mail.send(msg)
            flash('Your email has been saved and a confirmation email has been sent!', 'success')
        except Exception as e:
            flash(f'Error while sending email: {str(e)}', 'danger')

        # Redirect to the dashboard after successful submission
        return redirect(url_for('dashboard'))

    flash('Please enter a valid email address.', 'danger')
    return redirect(url_for('index'))

# Route for the subscription form submission
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    print(url_for('subscribe'))

    if email:
        # Validate email format
        try:
            valid = validate_email(email)  # This checks if the email format is valid
        except EmailNotValidError as e:
            flash(f"Invalid email address: {str(e)}", 'danger')
            return redirect(url_for('index'))

        # Store the email in the database (allowing duplicates)
        new_email = Email(email_address=email)
        try:
            db.session.add(new_email)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error while saving your email: {str(e)}', 'danger')
            return redirect(url_for('index'))

        # Send a confirmation email to the customer
        msg = Message('Thank you for subscribing!',
                      recipients=[email])
        msg.body = 'Thank you for subscribing to our newsletter. Stay tuned for updates.'
        try:
            mail.send(msg)
            flash('Your subscription is confirmed and a confirmation email has been sent!', 'success')
        except Exception as e:
            flash(f'Error while sending email: {str(e)}', 'danger')

        # Redirect to the dashboard after successful submission
        return redirect(url_for('dashboard'))

    flash('Please enter a valid email address.', 'danger')
    return redirect(url_for('index'))

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Fetch all emails from the database (including duplicates)
    emails = Email.query.all()
    return render_template('dashboard.html', emails=emails)  # Display the emails on the dashboard

if _name_ == '_main_':
    app.run(debug=True)
