import config
from __init__ import app
from timer import timer_aggregation_skywalking_core_interface

if __name__ == '__main__':
    timer_aggregation_skywalking_core_interface.do_async()
    app.run(
        host='0.0.0.0',
        port=config.app_conf["server"]["port"],
        debug=False
    )
