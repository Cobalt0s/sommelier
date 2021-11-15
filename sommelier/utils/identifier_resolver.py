from uuid import uuid4

from sommelier.logging import Judge, log_info


def create_alias(context, alias_id, identifier):
    if "flag_use_permanent_id" not in context:
        context.flag_use_permanent_id = None
    if context.flag_use_permanent_id is not None and context.flag_use_permanent_id:
        # This alias should be persisted for the whole test execution and should not be reset
        context.permanent_aliases[alias_id] = str(identifier)
        log_info(context, f"ID[{alias_id}] with Value[{str(identifier)}]")
    context.id_aliases[alias_id] = str(identifier)


def resolve_alias(context, alias_id):
    if alias_id in context.id_aliases:
        identifier = context.id_aliases[alias_id]
        if identifier is not None:
            return identifier

    # The assumption is that we never reach this code
    Judge(context).assumption(
        False,
        f'Alias "{alias_id}" is not found since no id is associated with it',
    )


def clear_aliases(context):
    context.id_aliases = {}
    if 'permanent_aliases' not in context:
        context.permanent_aliases = {}
    context.id_aliases = {**context.permanent_aliases}


def resolve_id_or_tautology(context, item):
    if item.startswith('$'):
        item = item[1:]
        if item.startswith('#'):
            # Generate Id
            return str(uuid4())
        return resolve_alias(context, item)

    return item
