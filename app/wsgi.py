import app.__init__ as flask_app

if __name__ == "__main__":
    app = flask_app.create_app()
    app.run()