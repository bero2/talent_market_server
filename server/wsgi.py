import pathlib
import site
from server.server import server

site.addsitedir(str(pathlib.Path(__file__).parent.parent.absolute()))


if __name__ == "__main__":
    server.run()
