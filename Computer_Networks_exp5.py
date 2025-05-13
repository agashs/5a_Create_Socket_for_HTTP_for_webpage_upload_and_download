#Name: A S Siddarth
#Reg No. 212224040316

import socket

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(4096).decode()
    return response

def upload_file(host, port, filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
        content_length = len(file_data)
        request = f"POST /upload HTTP/1.1\r\nHost: {host}\r\nContent-Length: {content_length}\r\nContent-Type: application/octet-stream\r\n\r\n"
        # Send the request headers followed by the file data in raw bytes
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.encode() + file_data)  # Send headers + file data
            response = s.recv(4096).decode()  # Get server's response
    return response

def download_file(host, port, filename):
    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    response = send_request(host, port, request)
    parts = response.split('\r\n\r\n', 1)  # Split header and body
    if len(parts) < 2:
        raise ValueError("Invalid HTTP response received.")
    file_content = parts[1]
    
    with open(filename, 'wb') as file:
        file.write(file_content.encode())  # Write the file content

if __name__ == "__main__":
    host = 'httpbin.org'
    port = 80
    
    # Upload file
    upload_response = upload_file(host, port, 'example.txt')
    print("Upload response:", upload_response)
    
    # Download file
    download_file(host, port, 'example.txt')
    print("File downloaded successfully.")
