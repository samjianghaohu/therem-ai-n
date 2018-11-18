#
# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from predict import generate_midi
import os
from flask import send_file, request
import pretty_midi
import sys
if sys.version_info.major <= 2:
    from cStringIO import StringIO
else:
    from io import StringIO
import time
import json

from flask import Flask
app = Flask(__name__, static_url_path='', static_folder=os.path.abspath('../static'))


@app.route('/predict', methods=['POST'])
def predict():
    now = time.time()
    # values = json.loads(request.data) #avenote reads input
    values = [77, 84, 104, 100, 0, 0, 0, 6, 0, 0, 0, 1, 1, 224, 77, 84, 114, 107, 0, 0, 0, 59, 0, 255, 81, 3, 7, 161, 32, 0, 144, 72, 127, 89, 144, 71, 127, 22, 128, 72, 90, 22, 144, 69, 127, 17, 128, 71, 90, 95, 128, 69, 90, 16, 144, 72, 127, 73, 144, 71, 127, 0, 128, 72, 90, 17, 144, 69, 127, 22, 128, 71, 90, 22, 128, 69, 90, 0, 255, 47, 0]
    print("the input data is loaded")
    print(values)
    # or we send in on our own
    # values = our_own_function()
    midi_data = pretty_midi.PrettyMIDI(StringIO(''.join(chr(v) for v in values)))
    print("midi file")
    print(midi_data)
    duration = float(request.args.get('duration'))
    ret_midi = generate_midi(midi_data, duration) #avenote send generated output
    return send_file(ret_midi, attachment_filename='return.mid',
        mimetype='audio/midi', as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    return send_file('../static/index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
