from imposc_actions import ImposcActions
import io
from pathlib import Path
from inspect import signature, Parameter
from flask import Flask, request, make_response, send_file, render_template
from markupsafe import Markup
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources=r'/*')
logging.getLogger('flask_cors').level = logging.DEBUG
logger = logging.getLogger('Impact oscillator service')
logger.level = logging.DEBUG

# TODO: look here https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files


def image_content_type(outfile: Path) -> str:
    return f"image/{outfile.suffix[1:]}"

def marshall_arguments(action_function, args: dict):
    outcome = []
    result = dict()

    sig = signature(action_function)

    for name, parameter in sig.parameters.items():
        if name == "kwargs":
            result.update(args)
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
                outcome.append(f"Parameter {name} was supplied with an invalid values {args[name]}")

    return result, outcome

@app.route('/')
def index():
    return 'Impact Oscillator'

@app.route('/<action>', methods=['POST', 'GET'])
def do_action(action):
    # Get method for action
    actions = ImposcActions()
    
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
                return make_response(render_template("error.html", message=f"No arguments supplied for {action}"), 422)

        except Exception as e:
            return make_response(render_template("error.html", message=f"{e}"), 400)

        logger.log(level=logging.DEBUG, msg=f"Args: {args}")

        # Marshall arguments
        marshalled_args, outcome = marshall_arguments(action_function, args)

        logger.log(level=logging.DEBUG, msg=f"Marshalled: {marshalled_args}")

        if outcome:
            message = Markup(f"<ul><li>{'<li>'.join(outcome)}</ul>")
            
            return make_response(render_template("error.html", message=message), 422)
        else:
            # Pass to function
            outfile: Path = action_function(**marshalled_args)

            if outfile.suffix == ".txt":
                # There was an error
                message = ""

                if outfile.exists():
                    message = outfile.read_text()

                return make_response(render_template("error.html", message=message), 422)
            else:
                # Return bytestream
                with outfile.open(mode = "rb") as image:
                    return send_file(
                                io.BytesIO(image.read()),
                                attachment_filename=f"{outfile}",
                                mimetype = image_content_type(outfile)
                        )
    else:
        return make_response(render_template("error.html", message=f"Unknown endpoint {action}"), 404)
