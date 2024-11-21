from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure Flask-Mail (SMTP server settings)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  # Load from environment
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Load from environment, default to 587 if not set
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Load from environment
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Load from environment
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')  # Load from environment

# Initialize Flask-Mail
mail = Mail(app)

# POST route for sending email
@app.route('/send-email', methods=['POST'])
def send_email():
    # Get message and email from the request JSON
    data = request.get_json()
    message_body = data.get('message')
    recipient_email = data.get('email')

    # Validate input data
    if not message_body or not recipient_email:
        return jsonify({'error': 'Message and email are required.'}), 400

    try:
        # Create the email message
        msg = Message(
            'Subject: Your Flask Email',  # Subject of the email
            recipients=[recipient_email]  # List of recipients
        )
        msg.body = message_body  # The body of the email

        # Send the email
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Email sent successfully!'}), 200
    except smtplib.SMTPException as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)