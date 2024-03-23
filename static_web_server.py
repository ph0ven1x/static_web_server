# 支持多用户同时访问
import socket
import urllib.parse
import threading


def handle_client_request(client_server_socket):
    # 获取从客户端发来的数据
    recv_client_data = client_server_socket.recv(4096)

    if len(recv_client_data) == 0:
        print("浏览器关闭了")
        client_server_socket.close()
        return

    # 将发来的二进制数据解码
    # utf-8解码后还要进行url解码
    recv_client_content = urllib.parse.unquote(recv_client_data.decode('utf-8'))
    print(recv_client_content)
    # 分割请求行
    request_list = recv_client_content.split(' ', maxsplit=2)

    # 获取请求资源路径
    request_path = request_list[1]
    print(request_path)
    if request_path == '/':
        request_path = '/index.html'
    # 动态打开指定文件内
    try:
        with open('./static' + request_path, 'rb') as file:
            # 读取文件内容
            file_data = file.read()
    except FileNotFoundError:
        # 请求资源部不存在返回404数据
        # 响应行
        response_line = 'HTTP/1.1 404 Not Found\r\n'
        # 响应头
        response_header = 'Server:PWS1.0\r\n'
        with open('./static/error.html', 'rb') as file:
            file_data = file.read()

        # 响应体
        response_body = file_data
        # 拼接响应报文
        response_data = (response_line + response_header + '\r\n').encode('utf-8') + response_body
        client_server_socket.send(response_data)
    else:
        # 响应行
        response_line = 'HTTP/1.1 200 OK\r\n'
        # 响应头
        response_header = 'Server:PWS1.0\r\n'
        # 响应体
        response_body = file_data
        # 拼接响应报文
        response_data = (response_line + response_header + '\r\n').encode('utf-8') + response_body
        # 发送响应数据
        client_server_socket.send(response_data)
        client_server_socket.close()
    finally:
        client_server_socket.close()


def main():
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口复用，程序退出，端口立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server_socket.bind(('', 8989))
    tcp_server_socket.listen(128)
    while True:
        # 等待接受客户端的连接请求
        client_server_socket, ip_port = tcp_server_socket.accept()
        print(ip_port)
        # 当客户端和服务器建立连接，创建子线程
        thread = threading.Thread(target=handle_client_request, args=(client_server_socket,))
        # 设置守护主线程
        thread.setDaemon(True)
        thread.start()


if __name__ == '__main__':
    main()
