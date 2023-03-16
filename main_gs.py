from groundstation.gui import GUI
from src.comms.radio import RF24

def do_led_flash(**kwargs):
    color = kwargs.get("led_color", "ALL")
    print(f"flashing {color} leds")

def do_take_picture(**kwargs):
    print("taking picture")

def do_send_message(**kwargs):
    entry = kwargs.get("entry", "default")
    message = entry.get()
    print(f"sending {message} to satellite")
    try:
        radio = RF24(1)
        radio.transmit(message)
    except:
        print("could not connect to radio!")

def main():
    
    # create an instance of a GUI
    gui = GUI()

    # populate the GUI with widgets 
    gui.make_fullscreen()
    gui.add_title("QSET MOC-SAT GROUND STATION")
    gui.add_button("Quit Application", gui.root.quit)
    gui.add_button("Flash LEDs", do_led_flash)
    gui.add_button("Take Picture", do_take_picture)
    message_entry = gui.add_entry("Message...")
    gui.add_button("Send Message", do_send_message, entry=message_entry)

    # run the gui application
    gui.run()

if __name__ == "__main__":
    main()