import telebot
from functions import generate_quiz

with open('bot_token.txt', 'r') as f:
    TOKEN = f.read()

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.last_name != None:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} {message.from_user.last_name} 😀 \n\n In this bot you can answer simple math questions. \n If you need /help click here.""")
    else:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} 😀 \n\n In this bot you can answer simple math questions. \n If you need /help click here.""")


@bot.message_handler(commands=['help'])
def help_response(message):
    bot.send_message(message.chat.id, 
                     f"""
The following commands are availabe:

/start -> Welcome message
/help -> Show Available Commands
/report -> Report This Bot
/quiz -> Start Quiz
...""")

@bot.message_handler(commands=['quiz'])
def start_quiz(messsage):
    user_data = {'step':1, 'score':0}
    sending_quiz(message=messsage, user_data=user_data)

def sending_quiz(message, user_data:dict):
    if user_data['step'] <= 5:
        quiz = generate_quiz()
        question, answer = quiz[0], quiz[1]

        bot.send_message(message.chat.id, f"step : {user_data['step']}/5 \n {question}")
        bot.register_next_step_handler(message, lambda msg: checking_answer(msg, answer, user_data))



def checking_answer(message, correct_answer, user_data):
    try:
        user_answer = int(message.text)
    except ValueError:
        bot.reply_to(message, "Invalid input 😔. \nPlease be careful! \nYou can restart on click /quiz ...")
    
    if user_answer == correct_answer:
        user_data['score'] += 1
    else:
      pass

    user_data['step'] += 1
    if user_data['step'] == 5+1:
        bot.send_message(message.chat.id, f"Quiz completed! Your final score: {user_data['score']}/5")
        return

    sending_quiz(message, user_data)

bot.infinity_polling()