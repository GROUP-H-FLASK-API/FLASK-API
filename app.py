from flask import Flask

#new instance(app instance) from the flask class
app= Flask(__name__) # creates the application
 #"the variable is used to it to represnt the name of the current model", Flask also uses it to know wjere to look for templates and static files
# it is also used to know if the python script is being run as the main program or if it is being  imported as a model in another python script

@app.route('/') # route method is a mapping btn a url and function to be executed when url passed in is acessed (taking two parameters e.g path/url and methods parameter ) 
#"the decorator tells flask to access a specific URL and invoked the decorated function , then return the result as responce to the client "
def home():
    return'<h2>Bright Jemimmah</h2>'


# if __name__ ** '__main__':
#     app.run(debug=True)
# if __name__ == '__main__':  #__name__ should be compared to __main__ using ==.the block to ensures that the app.run(debug = true )only runs when the script exists directly not when imported as a module.
#     app.run(debug=True)


