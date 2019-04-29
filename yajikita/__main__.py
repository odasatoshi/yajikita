from bottle import run
import sys

if len(sys.argv) == 1:
    import yajikita.app
    run(host='localhost', port=8080)
elif sys.argv[1] == 'init':
    from yajikita.user_master import initialize
    initialize()
else:
    print('unknown command: {}'.format(sys.argv[1:]))
