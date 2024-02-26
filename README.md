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
2. Open `config.yml` and complete with your MQTT server parameters 

3. Run the `mqtt_monitor.py` script from the command line:

    ```bash
    python mqtt_monitor.py
    ```