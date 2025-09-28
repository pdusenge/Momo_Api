# Momo API

A simple API for managing and analyzing mobile money (MoMo) transactions.

## Project Structure

```
Momo_Api/
├── api/
│   └── server.py           # Main API server implementation
├── data/
│   ├── modified_sms_v2.xml # Sample SMS data (XML)
│   └── transactions.json   # Sample transactions data (JSON)
├── dsa/
│   ├── comparison.py       # Data structure/algorithm comparison scripts
│   └── parser.py           # Data parsing utilities
├── docs/
│   └── api_docs.md         # API documentation
├── screenshots/            # API usage screenshots
│   ├── authorised_get.png
│   ├── Delete.png
│   ├── Post.png
│   ├── Put.png
│   └── unauthorisedAccess.png
└── README.md               # Project overview (this file)
```

## Features
- RESTful API for MoMo transactions
- Data parsing and analysis utilities
- Example data for testing
- API documentation and usage screenshots

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
Clone the repository:
	```bash
	git clone https://github.com/pdusenge/Momo_Api.git
	cd Momo_Api
	```
### Running the xml parser
which puts data in the dsa/transaction.json 
```bash
python dsa/parser.py
```

### Running the dsa comparison
```bash
python dsa/comparison.py
```

### Running the API Server
```bash
python api/server.py
```

The server will start on the default port (e.g., 5000). You can interact with the API using tools like Postman or curl.

## API Documentation
See [`docs/api_docs.md`](docs/api_docs.md) for detailed API endpoints and usage examples.

## Screenshots
Screenshots of API requests and responses are available in the `screenshots/` directory.

## License
This project is licensed under the MIT License.

## Author
- [pdusenge](https://github.com/pdusenge)
