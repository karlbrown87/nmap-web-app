# Nmap Web Application

This project is a web application that allows users to perform network scans using Nmap through a user-friendly web interface. The application is built with Flask and utilizes the python-nmap library to execute scans.

## Project Structure

```
nmap-web-app
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── templates
│   │   └── index.html
│   └── static
│       └── styles.css
├── requirements.txt
└── README.md
```

## Requirements

To run this application, you need to have Python installed along with the following dependencies:

- Flask
- python-nmap

You can install the required packages using pip:

```
sudo apt update
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libcairo2-dev
sudo apt install -y libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-dev
pip install -r requirements.txt
pip install weasyprint
```

## Usage

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the application:

```
python app/main.py
```

4. Open your web browser and go to `http://127.0.0.1:5000` to access the web interface.
5. Enter the target IP address or hostname and select the scan options.
6. Click on the "Scan" button to initiate the Nmap scan.
7. View the results displayed on the web interface.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and suggestions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.