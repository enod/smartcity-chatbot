from flask import Flask, request
from pymessenger2.bot import Bot
import os
from pymessenger2.buttons import URLButton, PostbackButton
from pymessenger2 import Element, QuickReply
import time


app = Flask(__name__)

ACCESS_TOKEN = "EAAKNq3yKyFoBADutBOzIwBYJiBE3tDVjSZA3gFQHChLd0XJmnm2lWqk5TmcZCN8iYheZCSP5GRMxZA6oQaZBrkX0JYejGUeX3jnnO4VL9LEM2LDeZAYl43ZBDC1ygg3a0o7o8m3tZC9GlC2a8pcrbLWphQO9Ku35kLGXppZCl6Vy59gZDZD"
VERIFY_TOKEN = "hi there"
bot = Bot(ACCESS_TOKEN, api_version='2.12')

welcome_msg = '''
Hello {}! I’m SMART CITY chatbot 🤖, I can offer you municipality service everywhere at any time. You can message me about road issues. 
'''
global dialogue
global story
dialogue = []
story = []
timeline = 0
seq = []

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            if event.get('messaging'):
                messaging = event['messaging']
                print(messaging)
                for x in messaging:
                    if x.get('message'):
                        recipient_id = x['sender']['id']
                        if x['message'].get('text'):
                            message = x['message']['text']
                            if message in ["hi", "hi there", "hello", "sain bainuu", "сайн уу", "hey", "yo"]:
                                buttons = []
                                button = URLButton(title='City live', url='http://103.17.108.244:1111/mjpg/video.mjpg')
                                buttons.append(button)
                                button = PostbackButton(title='Open ticket', payload='openticket')
                                buttons.append(button)
                                text = 'Choose a service please:' 
                                bot.send_image_url(recipient_id, "https://i.ytimg.com/vi/penG2V8bMBE/maxresdefault.jpg")
                                bot.send_text_message(recipient_id, welcome_msg.format(bot.get_user_info(recipient_id)['first_name']))
                                bot.send_button_message(recipient_id, text, buttons)
                                story.append('Story')
                            else:
                                print('printing story {}'.format(story))
                                if story == ['Story']:
                                    bot.send_text_message(recipient_id, 'Please enter your phone number:')
                                    story.append('Number')
                                elif story == ['Story', 'Number']:
                                    bot.send_text_message(recipient_id, 'Please describe the problem:')
                                    story.append('Description')
                                elif story == ['Story', 'Number', 'Description']:
                                    buttons = []
                                    button = QuickReply(content_type='location')
                                    buttons.append(button)
                                    message = 'Send your location'
                                    story.append('Location')
                                    bot.send_quick_reply(recipient_id, message, buttons)
                                        # elif story == ['Story', 'Number', 'Description', 'Location']:
                                            # bot.send_text_message(recipient_id, 'Please send a picture of a problem:')
                                    # story.append('Story')

                        if x['message'].get('attachments'):
                            print(x['message'])
                            if x['message']['attachments'][0]['type'] == 'location':
                                bot.send_text_message(recipient_id, 'Please send a picture of a problem:')
                            elif x['message']['attachments'][0]['type'] == 'image':
                                bot.send_text_message(recipient_id, 'Your ticket has been opened and we will get on it as fast as possible! Thank you.')
                                del story[:]

                            # if x['message']['attachments']['type'] == 'image':
                                # bot.send_text_message(recipient_id, 'Your ticket has been opened and we will get on it as fast as possible! Thank you.')



                    if x.get('postback'):
                        if x['postback']['payload'] == 'openticket':
                            recipient_id = x['sender']['id']
                            timeline = x['timestamp']
                            dialogue.append(timeline)
                            bot.send_text_message(recipient_id, 'Please enter your full name:')
                


        return "Success"


if __name__ == "__main__":
    app.run(port=5002, debug=True)

# "https://i.ytimg.com/vi/penG2V8bMBE/maxresdefault.jpg"
    
