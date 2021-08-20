import logging
import threading
import time

from rest.handle_skywalking_alarm import collection_date

logger = logging.getLogger('timer_aggregation_skywalking_core_interface')
logger.setLevel(logging.DEBUG)


def aggregate_alarm(current_times_collection_date):
    logger.debug(current_times_collection_date)


def timer_do_something():
    # logger.debug(collection_date)
    collection_date_length = len(collection_date)
    if collection_date_length < 1:
        return
    current_times_collection_date = []
    for i in range(0, collection_date_length):
        current_times_collection_date.append(collection_date.pop())
    aggregate_alarm(current_times_collection_date)


def do_something():
    while True:
        time.sleep(5)
        timer_do_something()


def do_async():
    threading.Thread(target=do_something).start()
