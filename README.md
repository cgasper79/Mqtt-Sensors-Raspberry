# Mqtt-Sensors-Raspberry
This is a simple Python program designed to monitor the temperature, last boot, CPU status and available memory on a Raspberry Pi and publish the data to an MQTT topic. It can be useful for monitoring system performance and taking action in case of overheating or high resource utilization.

## Requirements

- Python 3.x
- A Raspberry Pi with Raspbian or another compatible operating system

## Installation

1. Clone or download this repository to your Raspberry Pi.

    ```bash
    git clone https://github.com/cgasper79/Mqtt-Sensors-Raspberry.git
    ```

2. Navigate to the project directory.

    ```bash
    cd Mqtt-Sensors-Raspberry
    ```

3. Install dependencies if necessary.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Rename `example_config.yml` to `config.yml`
    ```bash
    mv example_config.yml config.yml
    ``` 
2. Open `config.yml` and complete with your MQTT server parameters, device configuration and update interval

    ```
    mqtt:
      broker: 'your_broker'
      port: 1883
      topic: 'your_topic'
      username: 'user'
      password: 'pass'

    deviceName: test 
    client_id: test
    timezone: Europe/Madrid
    update_interval: 1
    version_fw: 'v1.0'
    ```

3. Run the `mqtt_monitor.py` script from the command line:

    ```bash
    python mqtt_monitor.py
    ```

The program will display real-time information about CPU temperature, CPU usage, and available memory, and publish this data to an MQTT topic.

## Automatic Startup Configuration

To configure the Raspberry Pi Monitor to start automatically when the Raspberry Pi boots up, you can create a systemd service unit.

1. Create a new service unit file raspberry-pi-monitor.service in the /etc/systemd/system directory:

    ```bash
    sudo nano /etc/systemd/system/mqtt_monitor.service
    ``` 

2. Add the following configuration to the file:

   ```
   [Unit]
    Description=Raspberry Pi Monitor Mqtt
    After=network.target

    [Service]
    User=pi
    Type=idle
    ExecStart=/usr/bin/python3 /path/to/Mqtt-Sensors-Raspberry/mqtt_monitor.py
    WorkingDirectory=/path/to/Mqtt-Sensors-Raspberry

    [Install]
    WantedBy=multi-user.target
   ```
Replace /path/to/raspberry-pi-monitor with the actual path to your Raspberry Pi Monitor directory.

3. Save and close the file.

4. Reload systemd to load the new service unit:

    ```bash
    sudo systemctl daemon-reload
    ``` 

5. Enable the service to start on boot:

    ```bash
    sudo systemctl enable mqtt_monitor
    ``` 

6. You can use service to start, stop or restart:

    ```bash
    sudo service mqtt_monitor start
    sudo service mqtt_monitor stop
    sudo service mqtt_monitor restart
    sudo service mqtt_monitor enable
    ``` 


## Contributions

Contributions are welcome! If you have ideas for improvements or new features, please create a pull request or open an issue on this repository.
Acknowledgements

This project was inspired by the need to monitor the performance of my own Raspberry Pi. I thank the Raspberry Pi developer community for their ongoing work in improving and promoting this platform.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.