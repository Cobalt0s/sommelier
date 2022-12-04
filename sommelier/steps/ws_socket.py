from behave import given, when

from sommelier import WSocketManager


#
#
# Must instantiate WSocketManager to use these steps
#
#


@given('Connect as WS reader with cookie')
def connect_reader_ws(context):
    ws_manager: WSocketManager = context.ctx_manager.of(WSocketManager)
    ws_manager.create_socket(reader=True)


@given('Connect as WS writer with cookie')
def connect_writer_ws(context):
    ws_manager: WSocketManager = context.ctx_manager.of(WSocketManager)
    ws_manager.create_socket(reader=False)


@when('Read data from web-socket')
def read_ws(context):
    ws_manager: WSocketManager = context.ctx_manager.of(WSocketManager)
    ws_manager.read_data()


@when('Publish to web-socket')
def write_ws(context):
    ws_manager: WSocketManager = context.ctx_manager.of(WSocketManager)
    ws_manager.write_data()


@when('Disconnect from web-socket')
def disconnect_ws(context):
    ws_manager: WSocketManager = context.ctx_manager.of(WSocketManager)
    ws_manager.disconnect_all()
