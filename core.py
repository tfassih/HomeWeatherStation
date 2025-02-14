from typing import Optional
import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk, messagebox, StringVar


class HomeWeatherStationCore:
    UPDATE_DELAY = 500

    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("HOME WEATHER STATION")
        self.root.geometry("1280x720")
        self.serial_connection: Optional[serial.Serial] = None
        self.temperature = StringVar()
        self.temperature.set('0')
        self.humidity = StringVar()
        self.humidity.set('0')
        self.thermistor = StringVar()
        self.thermistor.set('0')

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack()

        ttk.Label(self.main_frame, text="Serial Port: ").pack()
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(self.main_frame, textvariable=self.port_var)
        self.port_combo.pack()

        self.connect_btn = ttk.Button(self.main_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack()

        ttk.Button(self.main_frame, text="↻", command=self.refresh_ports, width=5).pack()

        ttk.Label(self.main_frame, text="DHT11 SENSOR TEMPERATURE READING: ",
                  font=('Arial', 16, 'bold')).pack()
        self.THLabel = ttk.Label(self.main_frame, textvariable=self.temperature)
        self.THLabel.pack()
        self.schedule_update(self.THLabel, self.get_temperature)

        ttk.Label(self.main_frame, text="DHT11 SENSOR HUMIDITY READING: ",
                   font=('Arial', 16, 'bold')).pack()
        self.HHLabel = ttk.Label(self.main_frame, textvariable=self.humidity)
        self.HHLabel.pack()
        self.schedule_update(self.HHLabel, self.get_humidity)

        ttk.Label(self.main_frame, text="THERMISTOR READING: ",
                   font=('Arial', 16, 'bold')).pack()
        self.THERM_Label = ttk.Label(self.main_frame, textvariable=self.thermistor)
        self.THERM_Label.pack()
        self.schedule_update(self.THERM_Label, self.get_thermistor)


    def toggle_connection(self):
        if self.serial_connection is None:
            try:
                port = self.port_var.get()
                print(port)
                self.serial_connection = serial.Serial(port, 115200, timeout=1)
                self.connect_btn.config(text="Disconnect")
                messagebox.showinfo("SUCCESS", f"Connected to {port}")
            except serial.SerialException as e:
                messagebox.showerror("Error", f"Failed to connect: {str(e)}")
        else:
            self.serial_connection.close()
            self.serial_connection = None
            self.connect_btn.config(text="Connect")

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
            print(ports)

    def get_update_data(self):
        if self.serial_connection is not None:
            col = []
            i = 0


            while i < 3:
                data = self.serial_connection.readline().decode().strip()
                if not 'T/H' in data and i == 0:
                    break
                if 'T/H' in data:
                    data = data[3:]
                col.append(data)
                i = i + 1

            if col and all(x != '' and x is not None for x in col):
                print(col)
                return col

    def get_temperature(self):
        """Fetch and update temperature readings."""
        data = self.get_update_data()
        self.temperature.set(data[0] + ' °F' if data else '0 °F')

    def get_humidity(self):
        data = self.get_update_data()
        self.humidity.set(data[1] + ' %' if data else '0 %')

    def get_thermistor(self):
        data = self.get_update_data()
        self.thermistor.set(data[2] + ' °F' if data else '0 °F')

    def schedule_update(self, target_widget, callback):
        target_widget.after(self.UPDATE_DELAY, callback)


def schedule_temperature_update(app):
    """Schedule periodic temperature updates."""
    app.get_temperature()
    app.root.after(5000, schedule_temperature_update, app)  # Reschedule after 1000 ms

def schedule_humidity_update(app):
    """Schedule periodic humidity updates."""
    app.get_humidity()
    app.root.after(5000, schedule_humidity_update, app)  # Reschedule after 1000 ms

def schedule_thermistor_update(app):
    """Schedule periodic thermistor updates."""
    app.get_thermistor()
    app.root.after(2000, schedule_thermistor_update, app)  # Reschedule after 1000 ms

def main():
    root = tk.Tk()
    app = HomeWeatherStationCore(root)
    schedule_temperature_update(app)
    schedule_humidity_update(app)
    schedule_thermistor_update(app)
    root.mainloop()


if __name__ == "__main__":
    main()



### old sys code
# os.system('cls')
# for e in col:
#     print(e)
# machine = serial.Serial(port='COM6', baudrate=9600, timeout=.1)
# ports = serial.tools.list_ports.comports()
# choices = []
# print('PORT\tDEVICE\t\t\tMANUFACTURER')
#
# for index, value in enumerate(sorted(ports)):
#     if value.hwid != 'n/a':
#         choices.append(index)
#         print(index, '\t\t', value.name, '\t\t\t', value.manufacturer)

# while True:
#     col = []
#     i = 0
#     time.sleep(0.5)
#
#     while i < 3:
#         data = machine.readline()
#         str_data = data.decode('utf-8', 'ignore')
#         if not 'T/H' in str_data and i == 0:
#             break
#         col.append(str_data)
#         i = i + 1
#         time.sleep(0.5)
#     if [x != '' for x in col]:
#         os.system('cls')
#         for e in col:
#             print(e)




