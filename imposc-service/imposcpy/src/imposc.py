from imposc_actions import ImposcActions
import io
from pathlib import Path
from inspect import signature, Parameter
from flask import Flask, request, make_response, send_file, render_template, jsonify, abort
from markupsafe import Markup
from flask_cors import CORS
import logging
import sys

app = Flask(__name__)
CORS(app)

# Set up logging
sh = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
sh.setFormatter(formatter)

flask_logger = logging.getLogger('flask_cors')
flask_logger.setLevel(logging.DEBUG)
logger = logging.getLogger('Impact oscillator service')
logger.setLevel(logging.DEBUG)
flask_logger.addHandler(sh)
logger.addHandler(sh)

actions = ImposcActions()

# TODO: look here https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files


def image_content_type(outfile: Path) -> str:
    return f"image/{outfile.suffix[1:]}"

def marshall_arguments(action_function, args: dict):
    outcome = []
    result = dict()

    sig = signature(action_function)

    for name, parameter in sig.parameters.items():
        if name == "kwargs":
            validated, kwoutcome = actions.validate(args)
            result.update(validated)
            outcome.extend(kwoutcome)
        elif name not in args:
            # Not supplied - is there a default value?
            if parameter.default == Parameter.empty:
                outcome.append(f"Parameter {name} was not supplied")
        else:
            # Check type
            try:
                if str(parameter.annotation) == "<class 'float'>":
                    result[name] = float(args[name])
                elif str(parameter.annotation) == "<class 'int'>":
                    result[name] = int(args[name])
                else:
                    result[name] = args[name]
            except ValueError:
                outcome.append(f"Parameter {name} was supplied with an invalid value {args[name]}")

    return result, outcome

@app.errorhandler(422)
def bad_arguments(message: str):
    logger.log(level=logging.ERROR, msg=message)
    return jsonify(error=str(message)), 422

@app.errorhandler(400)
def bad_request(message: str):
    logger.log(level=logging.ERROR, msg=message)
    return jsonify(error=str(message)), 400

@app.errorhandler(404)
def bad_endpoint(message: str):
    logger.log(level=logging.ERROR, msg=message)
    return jsonify(error=str(message)), 404

@app.route('/')
def index():
    
    logger.log(level=logging.DEBUG, msg=f"Info request received")

    return jsonify(actions.info())

@app.route('/<action>', methods=['POST', 'GET'])
def do_action(action):
    # Get method for action
    
    logger.log(level=logging.DEBUG, msg=f"Action: {action}")

    action_function = getattr(actions, action, None)

    if action_function:

        try:
            # Get arguments from request
            if request.is_json:
                args = request.get_json()
                
            elif request.method == "POST":
                args = request.form

            elif request.method == "GET":
                args = request.args

            else:
                abort(422, f"No arguments supplied for {action}")

        except Exception as e:
            abort(400, f"{e}")

        logger.log(level=logging.DEBUG, msg=f"Args: {args}")

        # Marshall arguments
        marshalled_args, outcome = marshall_arguments(action_function, args)

        logger.log(level=logging.DEBUG, msg=f"Marshalled: {marshalled_args}")

        if outcome:
            message = Markup(f"<ul><li>{'<li>'.join(outcome)}</ul>")
            
            abort(422, message)
        else:
            # Pass to function
            outfile: Path = action_function(**marshalled_args)

            if isinstance(outfile, str):
                outfile = Path(outfile)

            if outfile.suffix == ".txt":
                # There was an error
                message = ""

                if outfile.exists():
                    message = outfile.read_text()

                return abort(422, message)
            else:
                # Return bytestream
                def send_file_kwargs(old_version=False):
                    """ Make sure the arguments to `send_file` are robust to changes in Python version """
                    file_key = "attachment_filename" if old_version else "download_name"
                    return {
                        file_key: f"{outfile}",
                        "mimetype": image_content_type(outfile)
                        }
                
                with outfile.open(mode = "rb") as image:
                    try:
                        return send_file(
                                    io.BytesIO(image.read()),
                                    **send_file_kwargs()
                            )
                    except TypeError:
                        return send_file(
                                    io.BytesIO(image.read()),
                                    **send_file_kwargs(True)
                            )
    else:
        return abort(404, f"Unknown endpoint {action}")
