import sys

payload = sys.argv[1]
eval(f'(sys.addaudithook(hook = (lambda x: lambda *_: x(1))(sys.exit)), {payload})')

sys.exit(0)
