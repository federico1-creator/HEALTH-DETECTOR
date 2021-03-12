from flaskserver import create_app

app = create_app()

if __name__ == '__main__':  # discorso bridge
    app.run(host='0.0.0.0', port=5000, debug=True)
