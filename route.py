def init(app):
    from rest import ping
    from rest import handle_skywalking_alarm

    # ################### 注册路由
    app.register_blueprint(ping.app)
    app.register_blueprint(handle_skywalking_alarm.app)
