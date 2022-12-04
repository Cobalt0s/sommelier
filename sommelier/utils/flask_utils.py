from flask import url_for, Flask


class FlaskUtils:

    @staticmethod
    def declare_route_site_map(application: Flask):
        def site_map():
            def has_no_empty_params(r):
                defaults = r.defaults if r.defaults is not None else ()
                arguments = r.arguments if r.arguments is not None else ()
                return len(defaults) >= len(arguments)

            links = []
            for rule in application.url_map.iter_rules():
                # Filter out rules we can't navigate to in a browser
                # and rules that require parameters
                if "GET" in rule.methods and has_no_empty_params(rule):
                    u = url_for(rule.endpoint, **(rule.defaults or {}))
                    links.append((u, rule.endpoint))
                # links is now a list of url, endpoint tuples
            return links, 200

        application.route("/site-map")(site_map)
