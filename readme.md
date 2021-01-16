## Simple python chat room, encrypted with using AES128
## How to Run? 
Run the `server.py` script from the command line. 

Usage: ```python3 server.py <host> [-p PORT]```

Arguments:
- ```host```: Interface the server listens at. Can be a hostname, or an IP address.
- ```-p PORT```: TCP port the server listens at (default 1060)

For example:

```bash
$ python3 server.py localhost
Listening at ('127.0.0.1', 1060)
```

Then run the `client.py` script from the command line and enter your password(in a separate terminal window). 

Usage: ```python3 client.py <host> [-p PORT]```

Arguments:
- ```host```: Interface the server listens at. Can be a hostname, or an IP address.
- ```-p PORT```: TCP port the server listens at (default 1060)

For example:

```bash
$ python3 client.py localhost
type your key: password
Your name: 
```
[chat room section is based on this repository](https://github.com/zeyu2001/pychat)

![alt text](https://github.com/alireza-roshanasan/crypto-chat/blob/master/pic.png)