from flaskblog import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    app.run(host="0.0.0.0",port=5000,debug=True)
