# 返回固定页面
import socket

if __name__ == '__main__':
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
        # 获取从客户端发来的数据
        recv_client_data = client_server_socket.recv(4096)
        # 将发来的二进制数据解码
        recv_client_content = recv_client_data.decode('utf-8')
        print(recv_client_content)

        with open('./static/index.html', 'rb') as file:
            # 读取文件内容
            file_data = file.read()

        # 相应行
        response_line = 'HTTP/1.1 200 OK\r\n'
        # 响应头
        response_header = 'Server:PWS1.0\r\nContent-Type: text/html\r\n\r\n'
        # 响应体
        response_body = file_data
        # 拼接响应报文
        response_data = (response_line + response_header + '\r\n').encode('utf-8') + response_body
        # 发送响应数据
        client_server_socket.send(response_data)
        client_server_socket.close()
