# Carrier Lookup Tool

A Python tool for performing bulk carrier lookups using the Ytel API. This tool takes a list of phone numbers and enriches them with carrier information including network provider, line type, location data, and more.

## Features

- **Bulk Processing**: Process up to 100 phone numbers in a single run
- **Rate Limiting**: Built-in rate limiting (10 transactions per second) to comply with API limits
- **Detailed Information**: Retrieves carrier name, line type (wireless/landline), city, state, zip code, and country
- **Error Handling**: Graceful error handling with detailed error messages
- **CSV Output**: Results exported to CSV format for easy analysis
- **Progress Tracking**: Real-time progress indicators during processing

## Prerequisites

- Python 3.7 or higher
- Ytel API key
- Internet connection

## Repository Structure

```
get-carrier/
├── carrier_lookup.py          # Main Python script
├── phone_numbers.csv          # Input CSV file (E.164 format)
├── phone_numbers_with_carrier.csv  # Output CSV file (generated)
├── requirements.txt           # Python dependencies
├── .env.ytel.example         # Example API key file
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd get-carrier
```

2. Install required dependencies:
```bash
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install requests python-dotenv
```

3. Create a `.env.ytel` file in the project directory and add your Ytel API key:
```bash
cp .env.ytel.example .env.ytel
# Then edit .env.ytel and replace YOUR_YTEL_API_KEY_HERE with your actual API key
```

Or create it directly:
```bash
echo "YOUR_YTEL_API_KEY" > .env.ytel
```

**Important**: Make sure to add `.env.ytel` to your `.gitignore` to keep your API key secure (already included in the provided `.gitignore`).

## Usage

### Input File

Create a CSV file named `phone_numbers.csv` with the following format:

```csv
phone_number
+14155552671
+12125551234
+13105559876
```

**Note**: Phone numbers must be in E.164 format (with `+` and country code).

### Running the Tool

Execute the script:

```bash
python3 carrier_lookup.py
```

### Output

The tool generates `phone_numbers_with_carrier.csv` with the following columns:

- `phone_number`: Original phone number
- `success`: Whether the lookup was successful (True/False)
- `carrier`: Carrier/network name (e.g., "Verizon Wireless", "T-Mobile")
- `line_type`: Type of line (wireless/landline)
- `city`: City associated with the phone number
- `state`: State/province code
- `zip_code`: ZIP/postal code
- `country`: Country code
- `raw_response`: Full API response (for debugging)
- `error`: Error message if lookup failed

### Example Output

```csv
phone_number,success,carrier,line_type,city,state,zip_code,country,raw_response,error
+14155552671,True,Verizon Wireless,wireless,San Francisco,CA,94102,US,...,
+14233812705,True,T-Mobile,wireless,Athens,TN,37303,US,...,
+16185126380,True,AT&T Illinois,landline,Granite City,IL,62002,US,...,
```

## Generating Random Phone Numbers

The repository includes a helper script to generate random US phone numbers for testing:

```bash
python3 -c "
import random
import csv

phone_numbers = []
for _ in range(100):
    area_code = random.randint(200, 899)
    exchange = random.randint(200, 999)
    subscriber = random.randint(0, 9999)
    phone_number = f'+1{area_code}{exchange}{subscriber:04d}'
    phone_numbers.append([phone_number])

with open('phone_numbers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['phone_number'])
    writer.writerows(phone_numbers)
"
```

**Note**: Randomly generated phone numbers may not be valid/assigned numbers and could fail carrier lookup.

## API Rate Limits

The tool is configured to respect Ytel API rate limits:
- Default: 10 transactions per second
- Configurable in `carrier_lookup.py` by modifying the `RATE_LIMIT` variable

## Configuration

You can modify the following variables in `carrier_lookup.py`:

```python
RATE_LIMIT = 10  # Transactions per second
API_BASE_URL = "https://api.ytel.com/api/v4/carrier/lookup"
```

## Error Handling

The tool handles various error scenarios:
- Invalid phone numbers
- API timeouts
- Network errors
- Authentication failures
- Rate limit errors

All errors are logged in the output CSV with detailed error messages.

## Troubleshooting

### "Invalid North American local phone number" Error

This error typically means:
- The phone number is not a valid/assigned number
- The phone number format is incorrect
- The number is outside North American numbering plan

### "API key not found" Error

Ensure your `.env.ytel` file exists and contains your API key on the first line.

### SSL/TLS Warnings

If you see `NotOpenSSLWarning`, this is typically harmless and won't affect functionality. To suppress:
```bash
python3 carrier_lookup.py 2>&1 | grep -v "NotOpenSSLWarning"
```

## Security Considerations

- **Never commit your API key** to version control
- Add `.env.ytel` to `.gitignore`
- Keep your API key secure and rotate it periodically
- Monitor your API usage to detect unauthorized access

## Sample .gitignore

```
.env.ytel
*.pyc
__pycache__/
phone_numbers_with_carrier.csv
.DS_Store
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built using the [Ytel API](https://api-docs.ytel.com/)
- Created for bulk carrier lookup operations

## Support

For issues or questions:
- Open an issue on GitHub
- Check Ytel API documentation: https://api-docs.ytel.com/

## Changelog

### Version 1.0.0
- Initial release
- Support for bulk carrier lookups
- Rate limiting implementation
- CSV input/output support
- Error handling and logging
