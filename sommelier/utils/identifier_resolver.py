import random
import string

from sommelier.logging import log_info
from sommelier.utils.string_manipulations import StringUtils


def create_alias(context_manager, alias_id, identifier):
    if context_manager.get('flag_use_permanent_id'):
        # This alias should be persisted for the whole test execution and should not be reset
        context_manager.set(f'permanent_aliases.{alias_id}', str(identifier))
        log_info(f"ID[{alias_id}] with Value[{str(identifier)}]")
    context_manager.set(f'id_aliases.{alias_id}', str(identifier))


def resolve_alias(context_manager, alias_id):
    identifier = context_manager.get(f'id_aliases.{alias_id}')
    if identifier is not None:
        return identifier

    # The assumption is that we never reach this code
    context_manager.judge().assumption(
        False,
        f'Alias "{alias_id}" is not found since no id is associated with it',
    )


def resolve_id_or_tautology(context_manager, item):
    if StringUtils.is_variable(item):
        item = StringUtils.extract_variable(item)
        if item == '#':
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        return resolve_alias(context_manager, item)

    return item
