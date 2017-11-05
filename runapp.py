import os

from paste.deploy import loadapp
from waitress import serve

<<<<<<< HEAD
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:production.ini', relative_to='.')

    serve(app, host='0.0.0.0', port=port)
=======
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:production.ini', relative_to='.')

    serve(app, host='0.0.0.0', port=port)
>>>>>>> d20aaa4a5520bb4a54930bd27bf6a55c0f6bb47c
