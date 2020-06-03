# Server Sent Events and HTTP requests Plugin for the thonny IDE

## Warning for Server Sent Events

The channels feature is not supported. If you want to send different events to different users, you should use the event type feature instead. Also, connections cannot be closed externally. The running thread has to be killed.

## Installation

- Install the python dependencies

```bash
pip install -r requirements.txt --user
```

## Start the plugin with thonny

```bash
cd /path/to/thonny/
PYTHONPATH=/path/to/thonny-sse_http_client/ python -m thonny
```

## Usage in thonny

To listen for Server Sent events click on the "Tools" section in the menu at the top of the program. And then select "Listen for SSE". You will be asked to input a URL. This server immeadiately echoes the message you send. For testing purposes you can use [this project](https://github.com/mchaov/simple-sse-nodejs-setup) and use the following URL: "http://localhost:5000/sse" To send HTTP GET requests you can click on the "Tools" section in the menu again and select "Send HTTP GET request" to send a message. After that, you will be asked for the URL. You can see all the communication on stdout.
