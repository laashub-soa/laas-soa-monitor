import base64
import json
import logging

from flask import Blueprint, request

from component import request_dingding_webhook

app = Blueprint('handle_sls_alarm', __name__,
                url_prefix='/handle_sls_alarm')
import config

dingding_webhook_access_token = config.app_conf["dingding_webhook_access_token"][0]
logger = logging.getLogger('sync_polardb_slow_log')
logger.setLevel(logging.DEBUG)
service_2_owner = {}
owner_2_service = config.app_conf["owner_2_service"]
owner_2_phone = config.app_conf["owner_2_phone"]
owner_2_name = config.app_conf["owner_2_name"]
serious_error_maximum_tolerance_count = config.app_conf["serious_error"]["maximum_tolerance_count"]
for (owner, service_list) in owner_2_service.items():
    for service_name in service_list:
        if not service_2_owner.__contains__(service_name):
            service_2_owner[service_name] = [owner]
        else:
            service_2_owner[service_name].append(owner)


@app.route('', methods=['POST'])
def handle_sls_alarm():
    at_mobiles = []
    try:
        logger.debug("handle request")
        api_token = request.args.get("api_token")
        is_at = request.args.get("is_at")
        if api_token != config.app_conf["api"]["token"]:
            return "api token was error"
        request_data = json.loads(request.get_data().decode())[0]
        start_time = request_data["StartTime"]
        end_time = request_data["EndTime"]
        raw_result_count = request_data["RawResultCount"]
        msg_template_prefix = "%s~%s %s个服务:\n" % (start_time, end_time, raw_result_count)
        raw_results = request_data["RawResults"]
        msg_template_details = "| 服务名称 | 异常次数 | 项目负责人 |\n\n" + "| -------- | -------- | ---------- |\n\n"
        for item in raw_results:
            service_name = item["service"]
            exception_count = item["exception_count"]
            query_sql = request_data["Query"]
            query_sql = query_sql[:query_sql.rfind("|")] + 'and service = "%s"' % service_name
            query_sql_base64 = base64.b64encode(query_sql.encode('utf-8')).decode()
            query_url = request_data["QueryUrl"]
            querystring_str = "&queryString="
            query_url_prefix = query_url[:query_url.find(querystring_str)]
            query_url_suffix = query_url[query_url.find(querystring_str) + len(querystring_str):]
            query_url_suffix = query_url_suffix[query_url_suffix.find("&"):]
            service_details_log_url = query_url_prefix + query_url_suffix + querystring_str + query_sql_base64
            service_display_name = "[%s](%s)" % (service_name, service_details_log_url)
            global service_2_owner
            global owner_2_phone
            global owner_2_name
            owner_code = service_2_owner[service_name][0]
            owner_phone = owner_2_phone[owner_code]
            if owner_phone not in at_mobiles:
                if is_at != str(1):
                    if exception_count >= serious_error_maximum_tolerance_count:
                        at_mobiles.append(owner_phone)
                else:
                    at_mobiles.append(owner_phone)
            service_owner_name = "@%s" % owner_phone

            msg_template_details += "| %s        | %s        | %s\n\n" % (
                service_display_name, exception_count, service_owner_name)
        title = msg_template_prefix
        msg_template_details = title + "\n" + msg_template_details
        logger.debug(msg_template_details)
    except BaseException as e:
        import traceback, sys
        traceback.print_exc()  # 打印异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

        msg_template_details = error
    dingding_resp = request_dingding_webhook.request_dingding_webhook(dingding_webhook_access_token, "服务异常日志",
                                                                      msg_template_details, at_mobiles)
    logger.debug(dingding_resp)
    return ""
