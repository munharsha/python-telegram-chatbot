#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from random import randint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Pickup Location', 'Pickup Time'],
                  ['Vacancy Left', 'Drop Off Location'],
                  ['Distance', 'Temperature'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    print(update.message)
    telegram_handle = update.message['chat']['username']
    update.message.reply_text(
        "Hi! @"+telegram_handle+', I\'m RVRC Carpool Bot and here to help you to find users to share the grab ride.' ,
        reply_markup=markup)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the Drop Off Location first.')


    return TYPING_CHOICE


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(" Just so you know, this is what you already told me:"
                              "{} You can tell me more, or change your opinion"
                              " on something.".format(facts_to_str(user_data)),
                              reply_markup=markup)

    return CHOOSING

def randomurl():
    x= ['https://ibb.co/5jZ3DrB','https://ibb.co/YkwjFzh' ,'https://ibb.co/86RHtys','https://scx1.b-cdn.net/csz/news/800/2016/carsharingin.jpg' ]
    return x[randint(0,3)]

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']
    if float(user_data['Temperature']) >=37.5:
        update.message.reply_photo('https://imgur.com/Cw7tCj7')
        update.message.reply_text('Sorry you will not be able to use our service in light of Covid-19')
        context.bot.send_message(chat_id=567967850, text='@'+ update.message['chat']['username']+' is having fever')
        context.bot.send_message(chat_id=-1001388440824,text='BEWARE @'+update.message['chat']['username']+' is having a fever')
        user_data.clear()
        return ConversationHandler.END

    update.message.reply_text("Telegram Handle @"+update.message['chat']['username']+
                              "{}"
                              "\n\nPlease add your handle to join the ride!".format(facts_to_str(user_data)))
    while True:
        try:
            update.message.reply_text('You have saved '+ str(float(user_data['Distance'])*189)+'grams of carbon dioxide if you have a fully booked car of 4 people!')
            update.message.reply_text('You have saved '+ str(float(user_data['Distance'])*210)+'grams of carbon dioxide if you have a fully booked car of 6 people!')
            update.message.reply_photo(randomurl())
            break
        finally:
            context.bot.send_message(chat_id=-1001388440824,text="Telegram Handle @"+update.message['chat']['username']+
                              "{}"
                              "\n\nPlease add your handle to join the ride!".format(facts_to_str(user_data)))
          

   

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1282281134:AAEMgXznRwbRs4I3QukUoNryacWEEnGKGEk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Pickup Location|Pickup Time|Vacancy Left|Drop Off Location|Distance|Temperature)$'),
                                      regular_choice)

                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice)
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information),
                           ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
