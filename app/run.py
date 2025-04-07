#importing our app instances from this file 
from app import creat_app #(the application factory function stores the app instance "create_app")
app = creat_app()

if __name__ == "__main__":
    app.run(debug=True)