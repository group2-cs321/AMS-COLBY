from website import create_app

#create a Flash app object
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port= 5000)
