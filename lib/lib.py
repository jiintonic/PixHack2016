
def reverse_url(url):
    arr = url.split('/')
    rev = ''
    for i in reversed(arr):
        rev += i + '/'
    rev = rev[0:-1]
    return rev
