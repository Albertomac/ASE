from flakon import JsonBlueprint
from flask import Flask, request, jsonify

calc = JsonBlueprint('calc', __name__)

@calc.route('/calc/sum', methods=['GET'])
def sum():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    result = m

    if n < 0:
        for i in range(n):
            result -= 1
    else:
        for i in range(n):
            result += 1

    return jsonify({'result': str(result)})