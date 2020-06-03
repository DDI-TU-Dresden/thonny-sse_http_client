from thonny import get_workbench
from threading import Thread
from tkinter.simpledialog import askstring
from sseclient import SSEClient
from requests import get
from requests import exceptions


class Singleton:
    """This Singleton class is needed because the list of SSE url strings is shared.
    __instance: The current instance of this class.
        """

    __instance = None

    @staticmethod
    def getInstance():
        """This is an unmodified Singleton.getInstance() method. It will create a new
        instance only once.
        
        Returns:
            Nested Singleton object with the list SSE url strings
        """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """This is an unmodified Singleton constructor. The singleton instance will
        contain an empty list.
        """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.sseList = []
            Singleton.__instance = self

    def get_sseList(self):
        """This method gets the list of SSE url strings.
        Returns:
            list of SSE url strings
        """
        return self.sseList

    def add_sse(self, url):
        """This method adds a SSE url string to the list.
        :param url: SSE url string
        Returns:
            None
        """
        self.sseList.append(url)


def send_request():
    """This method gets called if the "Send HTTP GET request" command is clicked
    in the "tools" menu. It will send a HTTP GET request to the specified URL.
    
        Returns:
            None
        """
    url = askstring("HTTP", "Which URL would you like to send the request to?")
    try:
        print("Sending HTTP GET request to " + url)
        response = get(url)
        print("Text received from " + url + " : " + response.text)
    except exceptions.ConnectionError:
        print("Failed to establish a new connection to " + url)


def listen_for_sse():
    """This method has to be called in a new thread because it blocks the current
    thread. It will listen for Server Sent Events and show them on stdout.
    Returns:
        None
    """
    urls = Singleton.getInstance().get_sseList()
    url = urls[len(urls) - 1]
    try:
        print("Connecting to SSE server " + url)
        messages = SSEClient(url)
        for msg in messages:
            print("Received SSE from server " + url)
            print("Data: " + msg.data)
            print("Event: " + msg.event)
            print("ID: " + msg.id)
    except exceptions.ConnectionError:
        print("Can't connect or lost the connection to the server " + url)


def add_sse_server():
    """This method gets called if the "Listen for SSE" command is clicked in the
    "tools" menu. It will get the Singleton instance and call the add_sse method with
    the given URL.
    
        Returns:
            None
        """
    url = askstring("SSE", "Which URL would you like to listen?")
    Singleton.getInstance().add_sse(url)
    t = Thread(target=listen_for_sse)
    t.daemon = True
    t.start()


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny. It will add the needed commands to the thonny workbench.
        Returns:
            None
        """
    get_workbench().add_command(
        command_id="sse_add",
        menu_name="tools",
        command_label="Listen for SSE",
        handler=add_sse_server,
    )
    get_workbench().add_command(
        command_id="http_send",
        menu_name="tools",
        command_label="Send HTTP GET request",
        handler=send_request,
    )
