from flask import current_app

APP_CODES = {
    100: "OK.",
    101: "Feature not implemented.",
    102: "Database error.",
    103: "Schema instance error.",
    104: "Input validation error.",
    105: "Resource not found.",
    106: "Resource busy.",
    107: "Empty data.",
}


def jsonify(state={}, metadata={}, status=200, code=100, headers={}):
    resource = {}
    resource["output"] = state
    resource["metadata"] = metadata
    resource["status"] = {"code": code}
    if current_app.debug is True:
        resource["status"]["message"] = APP_CODES[code]
    return resource, status, headers
