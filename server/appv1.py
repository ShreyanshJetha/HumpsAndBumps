
from flask import Flask, request, Response
# import graph
import time
import logging
import threading
import matplotlib.pyplot as plt
import json
#import multiprocessing

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

data_queue = []
start=None
end=None


@app.route('/api', methods = ['POST'])
def get_coordinates():
    
    global start, end, data_queue
    if not start:
        start=time.time()
    end=time.time()-start
    data_queue.append(json.loads(request.data.decode('utf-8')))
    print(data_queue[-1])
    return {'ok':True, 'status':200}

from tornado.ioloop import IOLoop
from bokeh.server.server import Server
from bokeh.embed import server_document

"""
# Function to get new data
def get_new_data():
    global data_queue, end
    seconds_count = end
    try:
        data = data_queue.pop(0)
        y = data['SpringFR']*100
    
        return [seconds_count], [y]
    except IndexError:
        return [seconds_count], [0]
"""
import random

# Function to get new data
def get_new_data():
    # Generate random x and y values
    x = [random.randint(0, 10)]
    y = [random.uniform(0, 10)]
    return x, y

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DataRange1d

# Initialize the plot
plot = figure(x_range=DataRange1d())

# Add a line glyph to the plot
line = plot.line(x=[], y=[])

# Create a ColumnDataSource for the line glyph
source = ColumnDataSource({'x': [], 'y': []})

# Set the line glyph's data source
line.data_source = source

# Function to update the plot
def update_plot():
    # Get new data
    x, y = get_new_data()

    # Update the ColumnDataSource with the new data
    source.stream(dict(x=x, y=y))

# Add a periodic callback to update the plot
curdoc().add_periodic_callback(update_plot, 1000)
curdoc().add_root(plot)
"""
# Show the plot
curdoc().add_root(plot)
"""
@app.route('/')
def index():
    # Generate the HTML code for the plot
    html = server_document(url='http://localhost:5006/app')
    return Response(html)

# Function to start the Bokeh server
def bk_worker():
    global plot
    # Start the Bokeh server
    server = Server({'/app': plot}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()

# Start the Bokeh server in a separate thread
threading.Thread(target=bk_worker).start()

app.run(port = 8000, host='0.0.0.0')