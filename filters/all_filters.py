import configparser

# Читает айди админа
config = configparser.ConfigParser()
config.read("settings.ini")
ADMIN = config["BOT"]["ADMIN"]
if ',' in ADMIN:
    ADMIN = ADMIN.split(",")
else:
    if len(ADMIN) >= 1:
        ADMIN = [ADMIN]
    else:
        print("ID админа не указан")

