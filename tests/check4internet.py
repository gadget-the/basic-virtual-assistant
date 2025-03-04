import requests, time

def connected_to_net(url = "http://www.kite.com/", timeout = 5):
    try:
        requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return False

# class connection_checker(object):
#     def __init__(self, check_url = "http://www.kite.com/") -> None:
#         self.check_url = check_url
#         self.timeout = 5

#     def connected_to_net(self):
#         try:
#             requests.get(self.check_url, timeout=self.timeout)
#             print("Connected to the Internet")
#             return True
#         except (requests.ConnectionError, requests.Timeout) as exception:
#             print("No internet connection.")
#             return False

class connection_checker(object):
    def __init__(self, check_url = "http://www.kite.com/", check_frequency = 60) -> None:
        ''' check_frequency: time inbetween internet connection checks '''
        self.check_url = check_url
        self.check_frequency = check_frequency
        self.timeout = 5
        self.is_connected = self.connected_to_net()
        self.running_checks = True

    def start(self):
        self.running_checks = True
        print("Starting...")
        self.check_loop()

    def stop(self):
        print("Stopping...")
        self.running_checks = False

    def connected_to_net(self):
        try:
            requests.get(self.check_url, timeout=self.timeout)
            print("Connected to the Internet")
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.")
            return False

    def check_loop(self):
        while self.running_checks:
            time.sleep(self.check_frequency)

            self.is_connected = self.connected_to_net()


if __name__ == "__main__":
    # connected_to_net()

    connection_checker_obj = connection_checker(check_frequency=30)
    connection_checker_obj.start()
    connection_checker_obj.stop()

'''
from https://www.kite.com/python/answers/how-to-check-internet-connection-in-python

thinking I could have this running at set intervals in a separate thread
    definitely not just a straight up while loop, there should be a pause-time set


from https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python

the first one from kite might have some problems
    the website that I use might block my IP if i ping it repeatedly
    some DNS stuff
    downloading the html from a website is an extra step that takes time
        if I use something else that just makes a connection/pings a website, it would be faster


randomized website ping?
    something that could be used to get around the problem of possibly getting banned from a website for trying to connect to it to often/quickly is using a different website each time
        well, this and having a longer interval between trying to connect
        though this would allow it to check for a connection more often

    it they could be randomly picked ot they could be cycled through in a specific order(or they could be randomly picked but then checked if it is the same website as the last time)


'''