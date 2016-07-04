from lib.pixnetdb import PixnetDB

def main():
    db = PixnetDB()
    num = db.get_article_count()
    print "PixnetDB contains %d articles." % num

if __name__ == '__main__':
    main()
