
# USDA 
# Torrence Washington
# July 2025

from phew import server, logging, access_point, dns, connect_to_wifi, is_connected_to_wifi
from phew.template import render_template
import json, sdcard, os, _thread, machine, utime, gc, network # type: ignore
from machine import SPI, Pin # type: ignore
gc.threshold(50000) # setup garbage collection

APP_TEMPLATE_PATH = "app_templates"
AP_NAME = "USAP"
WIFI_FILE = "wifi.json"
SETTINGS_FILE = "settings.json"
SD_MOUNT_PATH = '/sd'
SD_SAVES = 1
SPI_BUS = 0
SCK_PIN = 2
MOSI_PIN = 3
MISO_PIN = 4
CS_PIN = 5
onboard_led = machine.Pin("LED", machine.Pin.OUT)

# soft resets pico, working getting switch to work
def machine_reset():
    utime.sleep(5) # waits a second before going forward 
    print("Resetting...")
    machine.reset() # turns off pi

# starting page 
def app_index(request):
    return render_template(f"{APP_TEMPLATE_PATH}/index.html")

# configure the wifi connection
def app_configure(request):
    # writes save data from form onto a json file in string
    with open(WIFI_FILE, "w") as f:
        json.dump(request.form, f)
        f.close()
    # grabs library data from json file and uses it to connect to wifi 
    with open(WIFI_FILE) as f:
        wifi_credentials = json.load(f)
        ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"]) # get values of ssid and password to connect to wifi
    return render_template(f"{APP_TEMPLATE_PATH}/configured.html", ssid = wifi_credentials["ssid"], ip = ip_address)

# LED toggle, can ignore/delete
def app_toggle_led(request):
        onboard_led.toggle()
        return "OK"

def app_reset(request):
    """Immediately serves the reset page, then triggers async reset"""
    # Start reset sequence after small delay (allows page to load)
    _thread.start_new_thread(_delayed_reset, ())
    
    return render_template(
        f"{APP_TEMPLATE_PATH}/reset.html",
        access_point_ssid=AP_NAME,
        ip="192.168.4.1",  # Default AP IP
        reconnect_delay=3   # Seconds before auto-reconnect attempt
    )

def _delayed_reset():
    """Threaded reset with proper timing"""
    utime.sleep(1.5)  # Critical: Allow page to fully load first
    _perform_network_reset()

def _perform_network_reset():
    """Atomic reset operations"""
    try:
        # 1. Delete credentials
        if WIFI_FILE in os.listdir():
            os.remove(WIFI_FILE)
        
        # 2. Controlled disconnect
        wlan = network.WLAN(network.STA_IF)
        if wlan.isconnected():
            wlan.disconnect()
            utime.sleep(1)  # Allow graceful disconnect
            
        # 3. Ensure interface down
        wlan.active(False)
        utime.sleep(0.5)
        
        # 4. Restart AP
        global ap
        ap = access_point(AP_NAME)
        logging.info("AP restarted successfully")
        
    except Exception as e:
        logging.error(f"Reset failed: {str(e)}")

# options page 
def app_change_options(request):
    return render_template(f"{APP_TEMPLATE_PATH}/options.html")

def app_save_changes(request):
    # Save changes to settings file
    with open(SETTINGS_FILE, "w") as f:
        json.dump(request.form, f)
    
    # Attempt to transfer to SD card
    transfer_result = transfer_file_to_sd() if SD_MOUNTED else "SD card not available"
    
    # Get current SD card contents
    sd_files=list_sd_files()
    
    return render_template(f"{APP_TEMPLATE_PATH}/save_changes.html",
                         transfer_result=transfer_result,
                         sd_files=sd_files)

def view_saves(request):
    # Generate full HTML content in Python
    html_header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SD Card Files</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            a { color: #0066cc; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Files on SD Card</h1>
    """
    
    # Generate file links
    try:
        files = os.listdir(SD_MOUNT_PATH) # gets files from sd card
        file_links = ""
        for filename in files: # for loop to create hyperlinks for each file available
            file_links += f'<p><a href="/download/{filename}">{filename}</a></p>\n'
        if not files:
            file_links = "<p>No files found.</p>"
    except Exception as e:
        file_links = f"<p>Error: {str(e)}</p>"
    
    # Close HTML
    html_footer = """
        <br>
        <button onclick="window.location.href='/'">Go Home</button>
    </body>
    </html>
    """
    
    return server.Response(html_header + file_links + html_footer)

# temperature reader on pico, can ignore/delete
def app_get_temperature(request):
    # Not particularly reliable but uses built in hardware.
    # Algorithm used here is from:
    # https://www.coderdojotc.org/micropython/advanced-labs/03-internal-temperature/
    sensor_temp = machine.ADC(4)
    reading = sensor_temp.read_u16() * (3.3 / (65535))
    temperature = 27 - (reading - 0.706)/0.001721
    return f"{round(temperature, 1)}"

# Add this function to display SD card contents
def list_sd_files():
    try:
        files = os.listdir(SD_MOUNT_PATH)
        return "\n".join(files) if files else "No files found on SD card"
    except OSError:
        return "SD card not accessible"
# Modified transfer_file_to_sd() function
def transfer_file_to_sd():
    # 1. Check settings file
    try:
        with open(SETTINGS_FILE, 'r') as f:
            content = f.read()
            if not content.strip():
                return "No file to transfer (empty settings file)!\n" + list_sd_files()
            
            try:
                json.loads(content)  # Validate JSON
            except ValueError:
                return "Invalid JSON in settings file!\n" + list_sd_files()
    except OSError:
        return "No settings file to transfer!\n" + list_sd_files()

    # 2. Verify SD card
    if not SD_MOUNTED:
        return "SD card not mounted!\n" + list_sd_files()

    # 3. Find next available filename
    save_number = 1
    while True:
        new_filename = f"{SD_MOUNT_PATH}/save_settings{save_number}.json"
        try:
            with open(new_filename, 'r'):
                save_number += 1
        except OSError:
            break

    # 4. Write to SD card
    try:
        with open(new_filename, 'w') as f:
            f.write(content)
            f.close()
            
        # Return success message with updated file list
        return (f"Transfer successful! Saved to {new_filename}\n\n"
                f"Current SD card contents:\n{list_sd_files()}")
    except OSError as e:
        return f"Failed to write to SD card: {e}\n\nCurrent contents:\n{list_sd_files()}"

@server.route("/download/<filename>")
def download_file(request, filename):
    try:
        with open(f"{SD_MOUNT_PATH}/{filename}", "rb") as f:
            content = f.read()
        return server.Response(
            content,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return f"Error downloading file: {str(e)}", 404


# Update your SD card initialization to set SD_MOUNTED
try:
    spi = SPI(SPI_BUS, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
    cs = Pin(CS_PIN)
    sd = sdcard.SDCard(spi, cs)
    os.mount(sd, SD_MOUNT_PATH)
    print("SD card mounted successfully")
    print("Initial SD card contents:", list_sd_files())
    SD_MOUNTED = True

except Exception as e:
    print('SD card initialization failed:', e)
    SD_MOUNTED = False

def app_catch_all(request):
        return "Not found.", 404



# Routes to different pages
server.add_route("/", handler = app_index, methods = ["POST", "GET"])
server.add_route("/configure", handler = app_configure, methods= ["POST", "GET"])
server.add_route("/reset", handler = app_reset, methods = ["GET"])
server.add_route("/toggle", handler = app_toggle_led, methods = ["GET"])
server.add_route("/view", handler = view_saves, methods = ["GET"])
server.add_route("/temperature", handler = app_get_temperature, methods = ["GET"])
server.add_route("/options", handler = app_change_options, methods= ["POST", "GET"])
server.add_route("/savechanges", handler = app_save_changes, methods= ["POST", "GET"])


server.set_callback(app_catch_all)
# Set to Accesspoint mode
ap = access_point("USAP")  # Change this to whatever Wi-Fi SSID you wish
ip = ap.ifconfig()[0]                   # Grab the IP address and store it
logging.info(f"starting DNS server on {ip}")
dns.run_catchall(ip)                    # Catch all requests and reroute them
server.run()                            # Run the server
logging.info("Webserver Started")
