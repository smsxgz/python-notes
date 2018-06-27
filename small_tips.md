1. stdout.flush()
```python
import sys
for i in range(100):
    print('\r{}'.format(i), end='')
    sys.stdout.flush()
```

2. use an exception
```python
try:
    instance.attr.append('name')
except AttributeError:
    instance.attr = ['name']
```
Faster than using hasattr.

3. %
```python
print('%.2f%%' % (100/3))
```

4. How to haddle Ctrl-C with zmq
```python
import signal
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5558")

try:
    socket.recv()
except KeyboardInterrupt:
    print("W: interrupt received, stopping…")
finally:
    socket.close()
    context.term()
```

5. logging level

Level | Numeric value
------------ | -------------
CRITICAL | 50
ERROR | 40
WARNING | 30
INFO | 20
DEBUG | 10
NOTSET | 0


6. Debug
```python
from IPython import embed
embed()
```


7. Server file system
```bash
python2.7 -m SimpleHTTPServer 7999
```


8. psutil
Get process memory used.
```python
import psutil

process = psutil.Process(os.getpid())  
print('Memory used: {}'.format(process.memory_info().rss/1000000))
```


9.
