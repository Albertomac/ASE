from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.poll import Poll, NonExistingOptionException, UserAlreadyVotedException

doodles = JsonBlueprint('doodles', __name__)

_ACTIVEPOLLS = {} # list of created polls
_POLLNUMBER = 0 # index of the last created poll


@doodles.route('/doodles', methods=['GET', 'POST'])
def all_polls():

    if request.method == 'POST':
        result = create_doodle(request)

    elif request.method == 'GET':
        result = get_all_doodles(request)

    return result


@doodles.route('/doodles/<id>', methods=['GET', 'DELETE', 'PUT'])
def single_poll(id):
    global _ACTIVEPOLLS

    exist_poll(id) # check if the Doodle is an existing one

    if request.method == 'GET': # retrieve a poll
        result = jsonify(_ACTIVEPOLLS[id].serialize())

    elif request.method == 'DELETE':
        poll = _ACTIVEPOLLS.pop(id)
        _POLLNUMBER = sorted(_ACTIVEPOLLS.keys())[-1]
        result = jsonify({'winners': poll.get_winners()})

    elif request.method == 'PUT': 
        result = jsonify({'winners': vote(id, request)})

    return result


@doodles.route('/doodles/<id>/<person>', methods=['GET', 'DELETE'])
def person_poll(id, person):
    global _ACTIVEPOLLS

    exist_poll(id)

    if request.method == 'GET':
        result = jsonify({'votedoptions': _ACTIVEPOLLS[id].get_voted_options(person)})

    elif request.method == 'DELETE':
        result = jsonify({'removed': _ACTIVEPOLLS[id].delete_voted_options(person)})

    return result


def vote(id, request):
    global _ACTIVEPOLLS

    json_data = request.get_json()
    person = json_data['person']
    option = json_data['option']

    try:
        result = _ACTIVEPOLLS[id].vote(person, option)
    except (UserAlreadyVotedException, NonExistingOptionException):
        abort(400) # Bad Request

    return result


def create_doodle(request):
    global _ACTIVEPOLLS, _POLLNUMBER

    json_data = request.get_json()
    title = json_data['title']
    options = json_data['options']

    _POLLNUMBER += 1
    poll = Poll(_POLLNUMBER, title, options)
    _ACTIVEPOLLS[str(_POLLNUMBER)] = poll

    return jsonify({'pollnumber': _POLLNUMBER})


def get_all_doodles(request):
    global _ACTIVEPOLLS
    return jsonify(activepolls = [e.serialize() for e in _ACTIVEPOLLS.values()])


def exist_poll(id):
    global _ACTIVEPOLLS, _POLLNUMBER

    if int(id) > _POLLNUMBER:
        abort(404) # error 404: Not Found, i.e. wrong URL, resource does not exist

    elif not(id in _ACTIVEPOLLS):
        abort(410) # error 410: Gone, i.e. it existed but it's not there anymore
