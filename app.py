from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers import guess_lexer

app = Flask(__name__)

@app.route('/pygmentCode', methods=['POST'])
def pygment_code():
    if not request.json:
        abort(400)

    lexer = get_lexer_by_name(request.json['lexer'], stripall=True)
    formatter = HtmlFormatter(linenos=False)
    result = highlight(request.json['code'], lexer, formatter)
    return jsonify({'result': result}), 201


@app.route('/guessCode', methods=['POST'])
def guess_code():
    if not request.json:
        abort(400)

    lexer = guess_lexer(request.json['code'])
    print(lexer.name)
    return jsonify({'result': lexer.name}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)