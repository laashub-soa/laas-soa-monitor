def init(app):
    from rest import ping
    from rest import handle_sls_alarm

    # ################### 注册路由
    app.register_blueprint(ping.app)
    app.register_blueprint(handle_sls_alarm.app)
