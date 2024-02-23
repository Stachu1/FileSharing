from flask import Flask, send_file
from PIL import Image
import os, socket, logging, sys, click, qrcode, time
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


use_emoji = True
if (len(sys.argv) >= 3):
    if (sys.argv[2] == "--no-emoji"):
        use_emoji = False
sqr_white = "⬜"
sqr_black = "⬛"



def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = echo

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class background:
   BLACK = '\u001b[40m'
   WHITE = ' \u001b[47m'
   END = '\033[0m'


def check_file_path():
    if (len(sys.argv) >= 2):
        if (not os.path.exists(sys.argv[1])):
            print(f"{color.RED}{color.BOLD}{sys.argv[1]} not found!{color.END}")
            exit()
        return f"{os.getcwd()}/{sys.argv[1]}"
    else:
        print(f"{color.RED}{color.BOLD}File path not specified!{color.END}")
        exit()
    return None


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_port():
    s = socket.socket()
    s.bind(("", 0))
    return s.getsockname()[1]


def link(url, label=None):
    if label is None: 
        label = url
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"


def print_status():
    ip = get_ip()
    if port != 80:
        url = f"http://{ip}:{port}/"
    else:
        url = f"http://{ip}/"
    
    lines = [
    f"{color.CYAN}{color.BOLD}Sharing: {color.END}{color.CYAN}{file_path}{color.END}",
    f"{color.GREEN}{color.BOLD}IP address: {color.END}{color.GREEN}{ip}{color.END}",
    f"{color.YELLOW}{color.BOLD}Port: {color.END}{color.YELLOW}{port}{color.END}",
    f"{color.BOLD}URL: {color.END}{color.UNDERLINE}{link(url)}{color.END}"]
    
    message_length = len(max([f"Sharing: {file_path}", f"IP address: {ip}, Port: {port}, URL: {url}"], key=len))
    
    qr = generate_qrcode(url)
    print_output(qr, lines, message_length)
    
    
def generate_qrcode(url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="white", back_color="black")
    qr_image = qr_image.convert("L")
    return qr_image
    
    
def print_output(qr_image, lines, message_length):
    width, height = qr_image.size
    lines_count = len(lines)
    terminal_width = os.get_terminal_size().columns
    print_below = terminal_width < (width*2 + message_length)
    print(terminal_width, width*2, message_length)
    for y in range(height):
        row = []
        for x in range(width):
            if (qr_image.getpixel((x, y)) > 128):
                if use_emoji:
                    print(sqr_white, end="")
                else:
                    print("\033[1;4;21;37;47;51m" + ".." + "\033[0m", end=color.END)
            else:
                if use_emoji:
                    print(sqr_black, end="")
                else:
                    print("\033[1;4;21;30;40;51m" + ".." + "\033[0m", end=color.END)
                    
        
        if y+1 != height:
            if (lines_count > y and not print_below):
                print(lines[y])
            else:
                print()
        else:
            print("", end="\r") 
    
    if print_below:
        for line in lines:
            print(line)


app = Flask(__name__)


@app.route('/')
def index():
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        print(f"{color.RED}{color.BOLD}File not found!{color.END}")
        return "File not found", 404


if __name__ == '__main__':
    file_path = check_file_path()
    port = 80
    print_status()
    try: 
        app.run(host='0.0.0.0', port=port)
    except:
        port = get_port()
        app.run(host='0.0.0.0', port=port)