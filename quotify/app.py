from flask_restful import Api
from blueprints import app #, manager
import logging, sys
from logging.handlers import RotatingFileHandler


from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

api = Api(app, catch_all_404s=True)

# bagian atasnya dikurangin jadi kayak di atas doang

# use with @local / w5d1 /env

if __name__ == '__main__':
    ## nanti dikasih blueprint, dan db, ini untuk ngerun manage
    try:
        if sys.argv[1] == 'db':
            manager.run()
    ## nyoh
    except Exception as e:
        #normal run kalau tanpa argumen db
        formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        
        ## now app.root_path nya pindah tempat, tempat nyimpen lognya juga harus dipindah
        ## karena app-flask ada di __init__.py nya si blueprint yang begitu lah pokoknya
        log_handler = logging.handlers.RotatingFileHandler("%s/%s" %(app.root_path, '../storage/log/app.log'),maxBytes=10000, backupCount=10) 

        logging.getLogger().setLevel('INFO')

        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

        app.run(debug=True, host='0.0.0.0', port=5000)
