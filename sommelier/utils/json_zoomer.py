def zoom_in_json(json, zoom):
    keys = [x for x in f"{zoom}.".split('.')][:-1]
    given_value = None
    for key in keys:
        try:
            if given_value is None:
                given_value = json[key]
            else:
                given_value = given_value[key]
        except (KeyError, TypeError):
            if len(keys) == 1:
                raise Exception(f'No key "{zoom}" in json {json}')
            raise Exception(f'Invalid zoom "{zoom}" failed at "{key}" in json {given_value}')
    return given_value
