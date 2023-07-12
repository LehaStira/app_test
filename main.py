from flask import Flask

from controllers.user_controller.user import user_routes

app = Flask(__name__)


app.register_blueprint(user_routes)


if __name__ == "__main__":
    app.run(port=5111)
