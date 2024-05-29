from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database setup
engine = create_engine('sqlite:///users.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

# Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt', padding=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=50,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()

    if 'i want to log in' in incoming_msg:
        session['step'] = 'get_email'
        response.message('Please enter your email:')
    elif session.get('step') == 'get_email':
        session['email'] = incoming_msg
        session['step'] = 'get_password'
        response.message('Please enter your password:')
    elif session.get('step') == 'get_password':
        session['password'] = incoming_msg
        try:
            # Save to the database
            new_user = User(email=session['email'], password=session['password'])
            db_session.add(new_user)
            db_session.commit()
            response.message('Your account has been registered.')
        except SQLAlchemyError as e:
            db_session.rollback()
            response.message('There was an error registering your account.')
        finally:
            session.pop('step', None)
            session.pop('email', None)
            session.pop('password', None)
    else:
        response.message(generate_response(incoming_msg))

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
