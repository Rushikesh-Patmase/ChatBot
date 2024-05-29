# ChatBot
A chatbot made using Flask which responds to a user when he says "i want to login" and asks for their email and password and also stores them in the database.

# Steps to Run Your Flask Application

## 1. Activate Your Virtual Environment:

      new_env\Scripts\activate

## 2. Install Required Packages:
Ensure all the required packages are installed in your virtual environment:

pip install flask twilio transformers torch sqlalchemy


## 3. Run Your Flask Application:
Start the Flask server:

flask run

## 4. Setting Up Ngrok and Configuring Twilio
Start Ngrok:

Open a new terminal window and run:

ngrok http 5000


## 5. Copy the Ngrok URL:

Ngrok will provide a forwarding URL like http://<your_ngrok_subdomain>.ngrok.io. Copy this URL.

## 6. Configure Twilio:

* Log in to your Twilio account.

* Navigate to the WhatsApp sandbox settings.

* Set the When a message comes in URL to the Ngrok forwarding URL followed by /sms. For example: http://<your_ngrok_subdomain>.ngrok.io/sms.

* Save the settings.

* Testing Your Chatbot

## 7. Send a WhatsApp Message:

Use your WhatsApp application to send a message to your Twilio WhatsApp sandbox number. Start with "i want to log in" and follow the prompts.

## 8. Monitor Flask Logs:

Keep an eye on the Flask application logs to see the interactions and debug any issues if necessary.
