# import pathlib
# import site
# from server.server import server
#
# site.addsitedir(str(pathlib.Path(__file__).parent.parent.absolute()))
#
#
# if __name__ == "__main__":
#     server.run()


from server import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
