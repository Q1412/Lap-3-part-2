from socket import *
import ssl
import base64


# Choose a mail server (e.g. Google mail server) and call it mailserver mailserver
mail_server = "smtp.gmail.com"
port = 587
server_port = (mail_server, port)
end_msg = "\r\n.\r\n"
user = "quyennln1412@gmail.com"
password = "<remove for privacy>" # this is an gmail app login password.
dest_email = "baohoang_1812@yahoo.com"

# Create socket called clientSocket and establish a TCP connection with mailserver
raw_socket = socket (AF_INET, SOCK_STREAM)
raw_socket.connect(server_port)

recv = raw_socket.recv(1024).decode() 
print("CONNECT", recv)


# Send HELO command and print server response. 
heloCommand = 'HELO Alice\r\n' 
raw_socket.send(heloCommand.encode())
recv = raw_socket.recv(1024).decode() 
print("HELO", recv)

# Send STARTTLS command to upgrade the connection
starttls_command = "STARTTLS\r\n"
raw_socket.send(starttls_command.encode())
recv = raw_socket.recv(1024).decode()
print("STARTTLS", recv)

# Upgrade to use SSL
ssl_client_socket = ssl.wrap_socket(raw_socket)

# Send HELO again with SSL client
ssl_client_socket.send(heloCommand.encode())
recv = ssl_client_socket.recv(1024).decode()
print('HELO again', recv)


# Log in with AUTH PLAIN
base64_str = ("\x00"+user+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
ssl_client_socket.send(authMsg)
recv = ssl_client_socket.recv(1024).decode()
print('AUTH ', recv)


# Send MAIL FROM command
mail_from = "MAIL FROM: <{}>\r\n".format(user)
ssl_client_socket.send(mail_from.encode())
recv = ssl_client_socket.recv(1024).decode()
print("MAIL FROM", recv)

# Send RCPT TO command and print server response.
rcpt_cmd = "RCPT TO:<{}>\r\n".format(dest_email)
ssl_client_socket.send(rcpt_cmd.encode())
recv = ssl_client_socket.recv(1024).decode()
print("RCPT TO", recv)

# Send DATA command and print server response.
data = "DATA\r\n"
ssl_client_socket.send(data.encode())
recv = ssl_client_socket.recv(1024).decode()
print("DATA", recv)

# Send message data.
ssl_client_socket.send(("Yes it works !!!!" + end_msg).encode())
recv = ssl_client_socket.recv(1024).decode()
print("Send data", recv)

# Send QUIT command and get server response.
quit = "QUIT\r\n"
ssl_client_socket.send(quit.encode())
recv = ssl_client_socket.recv(1024).decode()
print("Quit", recv)
ssl_client_socket.close()
