import json
import logging

from flask import Blueprint, request

app = Blueprint('handle_skywalking_alarm', __name__,
                url_prefix='/handle_skywalking_alarm')
import config

logger = logging.getLogger('handle_skywalking_alarm')
logger.setLevel(logging.DEBUG)

# 实时收集的数据
collection_date = []


def do_handle_sls_alarm(request_data):
    # 慢接口
    text_content = request_data["text"]["content"]
    if "接口超时1秒" not in text_content:
        return
    in_index = text_content.rfind(" in ") + 4
    service_name = text_content[in_index:]
    # print("service_name: ", service_name)
    to_index = text_content.find(" to ") + 4
    interface_name = text_content[to_index: in_index - 4]
    # print("interface_name: ", interface_name)
    globals
    collection_date.append({"service": service_name, "interface": interface_name})
    logger.debug(collection_date)


@app.route('', methods=['GET', 'POST'])
def handle_sls_alarm():
    logger.debug("handle request")
    api_token = request.args.get("api_token")
    if api_token != config.app_conf["api"]["token"]:
        return "api token was error"
    # print("args: ", request.args)
    request_data = request.get_data().decode()
    # print("data:", request_data)
    do_handle_sls_alarm(json.loads(request_data))
    return 'ok'
