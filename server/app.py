import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from copy import deepcopy
from flask import Flask, request
# import graph
import joblib
import time
import logging
import threading
import matplotlib.pyplot as plt
import json
#import multiprocessing
import os

STAGE = 'TEST' # TRAIN|TEST

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

data_queue = []
start=None
end=None

output_file = 'training.csv' if STAGE == 'TRAIN' else 'testing.csv'
# Load the model from the file
if STAGE == 'TEST':
    loaded_model = joblib.load('decision_tree_model.sav')


def update_dataset(new_data, index):
    df = pd.DataFrame(deepcopy(new_data), index=[index])
    df.to_csv(output_file, mode = 'a+', header = True if index == 1 else False)

@app.route('/api', methods = ['POST'])
def get_coordinates():
    
    global start, end, data_queue
    if not start:
        start=time.time()
    end=time.time()-start

    data_queue.append(json.loads(request.data.decode('utf-8')))
    threading.Thread(target= update_dataset,args = (data_queue[-1], len(data_queue),)).start()
    return {'ok':True, 'status':200}

threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=5000)).start()

# Set up the plot
fig, ax = plt.subplots()

# Set up the attributes. Excludes line, legend
attributes = {
    'SpringFR' : {'ydata': [], 'color': 'red'},
    'SpringFL': {'ydata': [], 'color': 'blue'}, 
    'WishboneTargetFR' : {'ydata': [], 'color': 'gold'}, 
    'WishboneTargetFL': {'ydata': [], 'color': 'green'}
}




for name, attribute in attributes.items():
    attribute['line'], = ax.plot([], [], lw=1, color=attribute['color'])
    # Initiate individual legend
    plt.plot([], [], color=attribute['color'], lw=1, markersize=1, label=name)

# Add state legend for prediction
if STAGE == 'TEST': 
    plt.plot([], [], color= 'black', lw=1, markersize=1, label='State')

# Spawn all legends
legend = plt.legend(loc=0)

print(attributes)
# Set up the data
xdata = []

# Set up the animation
start_time = time.time()
def update(num):
    global data_queue

    if not data_queue:
        return

    # Get the elapsed time
    elapsed_time = time.time() - start_time

    _last_data = data_queue[-1]

    # Use the model to make predictions
    if STAGE == 'TEST':
        try:
            del _last_data['state']
        except KeyError:
            pass

        X_test = pd.DataFrame(deepcopy(_last_data), index=[len(data_queue)])
        y_pred = loaded_model.predict(X_test)
        print(y_pred)
        # accuracy = accuracy_score(y_test, y_pred)
        # print(f"Accuracy: {accuracy}")

    # Update the data
    xdata.append(elapsed_time)

    # Update the plot
    for i, (name, attribute) in enumerate(attributes.items()):
        attribute['ydata'].append(_last_data[name])
        attribute['line'].set_data(xdata, attribute['ydata'])
        legend.get_texts()[i].set_text(f'{name} {_last_data[name]}')

    # Update State legend
    legend.get_texts()[4].set_text(f'State {y_pred[0]}')

    ax.relim()
    ax.autoscale_view()
    return (attribute['line'] for name, attribute in attributes.items())

ani = animation.FuncAnimation(fig, update, interval=100)

# Customize the x-axis
ax.set_xlabel("Time (s)")

# Show the elapsed time in seconds on the x-axis
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1f}"))

plt.show()
