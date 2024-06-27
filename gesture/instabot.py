from instabot import Bot
bot = Bot()
bot.login(username="sachin_jha_1822",password= "")
followers = bot.get_user_followers("Sachi_jha_1822")
for follower in followers:
    print(bot.get_user_info(follower))