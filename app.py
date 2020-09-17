#!flask/bin/python
from flask import Flask,jsonify,abort,make_response,request,url_for

app = Flask(__name__)

pitches = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/pitcher/api/v1.0/pitches', methods=['GET'])
def get_pitches():
    return jsonify({'pitches': pitches})

@app.route('/pitcher/api/v1.0/pitches/<int:pitch_id>', methods=['GET'])
def get_pitch(pitch_id):
    pitch = [pitch for pitch in pitches if pitch['id'] == pitch_id]
    if len(pitch) == 0:
        abort(404)
    return jsonify({'task': pitch[0]})

@app.route('/pitcher/api/v1.0/pitches', methods=['POST'])
def create_pitch():
    if not request.json or not 'title' in request.json:
        abort(400)
    pitch = {
        'id': pitches[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    pitches.append(pitch)
    return jsonify({'pitch': pitch}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/pitcher/api/v1.0/pitches/<int:pitch_id>', methods=['PUT'])
def update_pitch(pitch_id):
    pitch = [pitch for pitch in pitches if pitch['id'] == pitch_id]
    if len(pitch) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    pitch[0]['title'] = request.json.get('title', pitch[0]['title'])
    pitch[0]['description'] = request.json.get('description', pitch[0]['description'])
    pitch[0]['done'] = request.json.get('done', pitch[0]['done'])
    return jsonify({'pitch': pitch[0]})

@app.route('/pitcher/api/v1.0/pitches/<int:pitch_id>', methods=['DELETE'])
def delete_pitch(pitch_id):
    pitch = [pitch for pitch in pitches if pitch['id'] == pitch_id]
    if len(pitch) == 0:
        abort(404)
    pitches.remove(pitch[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)