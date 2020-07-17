from app.app import create_app
from app.config import Config


from logging.config import dictConfig

dictConfig(Config.LOGGER)


app = create_app(config_class=Config)


if __name__ == '__main__':
    app.run(debug=True)
