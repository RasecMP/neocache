import time
import network
from machine import Pin
from phew import server
from phew.template import render_template

led = Pin("LED", Pin.OUT)

def start_ap():
    
    # Set WIFI credentials.
    ssid = 'GEOCACHING'
    password = '12345678'

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    ap.active(False)
    ap.active(True)

    while not ap.active():
        print('Connecting...')
    print('Connection successful')
    print(ap.ifconfig())

def main():
    
    start_ap()
    
    @server.route("/favicon.ico", methods=["GET"])
    def favicon(request):
        return render_template("favicon.ico"), 200
    
    @server.route("/logbook.txt", methods=["GET"])
    def logbook(request):
        return render_template("logbook.txt"), 200
    
    @server.route("/", methods=["GET"])
    def index(request):
        return render_template("index.html"), 200
    
    @server.route("/", methods=["POST"])
    def index_post(request):

        username = request.form.get("username", None)
        date = request.form.get("date", None)
        
        with open("logbook.txt", "r+") as logbook:
            logbook_lines = logbook.readlines()
            found = any(line.split()[1] == username for line in logbook_lines)

            if not found:
                log_line = "{} {}\n".format(date, username)
                logbook.write(log_line)
                led.on()
                time.sleep(0.5)
                led.off()

        return render_template("index.html"), 200

    server.run()

if __name__ == '__main__':
    main()