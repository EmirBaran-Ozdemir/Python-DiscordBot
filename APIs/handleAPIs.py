from dotenv import load_dotenv
import dotenv


def configure():
    load_dotenv()


def addAPI(userName, userAPI):
    dotenv.set_key("APIs/.env", userName, userAPI)
