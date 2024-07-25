"""
启动界面
"""
from tornado import ioloop, web
import logging
import socket
from Ollama_Api.server import *

# 1.消息记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

args = {
    "db": None
}


# 2.配置app路由url
def make_app():
    # 路由
    application = [
        (r"/", Index),
        (r"/chat", ChatHandler),
    ]
    app = web.Application(application)

    # 打印每个路由的URL信息
    for route in application:
        logger.info(f"Configured route: {route[0]}")

    return app


if __name__ == '__main__':
    app = make_app()
    # 端口
    port = 5000
    app.listen(port, address='0.0.0.0')

    # 获取局域网IP地址
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # 事件的提示
    logger.info(f"Service started, listening on port {port}")
    logger.info(f"Accessible on http://{local_ip}:{port}")

    # 开始事件循环
    ioloop.IOLoop.current().start()
