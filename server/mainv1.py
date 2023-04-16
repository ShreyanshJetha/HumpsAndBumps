from flask import Flask, request
# import graph
import os
import sys
import time
import signal
import logging
import threading
import matplotlib.pyplot as plt

#import multiprocessing
# \Scripts\activate

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

start=None
end=None
data_x=[]
data_y=[]

@app.route('/api')
def get_coordinates():
    global start,data_x,data_y
    if not start:
        start=time.time()
    end=time.time()-start
    
    # print('Current\tdata\t:\t{}\t{}\t{}'.format(
    #     float(request.args.get('x').strip()),
    #     float(request.args.get('y').strip()),
    #     float(request.args.get('z').strip())
    # ), end='\r',flush=True)

    data_x.append(end)
    data_y.append(float(request.args.get('y')))
    # #graph.plot(end, float(request.args.get('y')))
    return {'ok':True, 'status':200}



if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=5000)).start()
    #app.run(host='0.0.0.0', port=5000)
    #sj@Sj:~$ kill -9 $(lsof -t -i tcp:5000)
    plt.figure() 
    ln, = plt.plot([],[],'*')
    plt.ion()
    plt.show()

    while True:
        try:
            #print(data_x)
            plt.scatter(data_x[-1], data_y[-1],marker='_')
            #plt.scatter(data_x[-1], data_y[-1])
            #plt.plot(data_x,data_y)
            plt.draw()
            plt.pause(0.001)

        except (ValueError, IndexError):
            pass
        except KeyboardInterrupt:
            plt.close()
            print('exiting')
        
    plt.close()
    print('exiting 2')
    sys.exit(0)
