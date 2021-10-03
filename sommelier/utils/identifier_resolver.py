from bson import ObjectId


def create_alias(context, alias_id, identifier):
    context.id_aliases[alias_id] = str(identifier)


def resolve_alias(context, alias_id):
    if alias_id in context.id_aliases:
        identifier = context.id_aliases[alias_id]
        if identifier is not None:
            return identifier

    raise Exception(f'Alias "{alias_id}" is not found since no id is associated with it')


def clear_aliases(context):
    context.id_aliases = {}


def resolve_id_or_tautology(context, item):
    if item.startswith('$'):
        item = item[1:]
        if item.startswith('#'):
            # Generate Id
            return str(ObjectId())
        return resolve_alias(context, item)

    return item
