def get_json(context):
    try:
        json = context.result.json()
        if json is None:
            raise KeyError
        return json
    except Exception:
        print("JSON is missing in response")
        print(context.result.text)
        assert False
