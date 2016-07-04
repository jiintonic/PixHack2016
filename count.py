from lib.pixnetdb import PixnetDB

def main():
    db = PixnetDB()
    count = db.get_article_count()
    print "PixnetDB contains %d articles." % count

    count = db.get_author_count()
    print "PixnetDB contains %d authors." % count

if __name__ == '__main__':
    main()
