import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = "database"

if __name__ == "__main__":
    if os.path.exists(os.path.join(basedir, '..', DATA_PATH)):
        print("database folder exist")
    else:
        os.mkdir(os.path.join(basedir, '..', DATA_PATH))
