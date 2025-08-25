# Checkmarx Report Generator

A Python utility for generating and sending customized security scan reports from Checkmarx Application Security Testing (AST) platform.

## Overview

This tool connects to the Checkmarx AST API to create detailed security scan reports with customizable sections and filters. Reports can be generated in multiple formats (PDF, JSON, CSV) and automatically sent via email to specified recipients.

## Features

- OAuth authentication with Checkmarx IAM
- Customizable report sections and filters
- Multiple output formats (PDF, JSON, CSV)
- Email delivery of reports
- Configurable severity and state filters
- Support for multiple scanner types (SAST, SCA, IaC, Containers)

## Prerequisites

- Python 3.6 or higher
- `requests` library
- Valid Checkmarx AST account with API access
- API key from Checkmarx platform

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd report-generator
```

2. Install required dependencies:
```bash
pip install requests
```

## Configuration

1. Copy the example configuration file:
```bash
cp example-config.json config.json
```

2. Edit `config.json` with your Checkmarx credentials:
```json
{
    "api_url": "https://us.ast.checkmarx.net/api",
    "iam_url": "https://us.iam.checkmarx.net/auth/realms/",
    "api_key": "your-api-key-here",
    "tenant_name": "your-tenant-name",
    "email_to": ["recipient@example.com"]
}
```

### Configuration Parameters

- **api_url**: Base URL for Checkmarx AST API
- **iam_url**: Checkmarx IAM authentication URL
- **api_key**: Your Checkmarx API key (refresh token)
- **tenant_name**: Your Checkmarx tenant identifier
- **email_to**: List of email addresses to receive reports

## Usage

### Basic Usage

Run the report generator with a scan ID:
```bash
python send_report.py <scan_id>
```

Example:
```bash
python send_report.py 9f740d6c-2f1a
```

To see available options:
```bash
python send_report.py --help
```

### Customizing Reports

The script generates reports with the following default configuration:

- **Report Type**: Email delivery
- **File Format**: PDF
- **Sections**: Scan information, results overview, scan results, resolved results, categories, vulnerability details
- **Scanners**: SAST, SCA, IaC, Containers, Microengines
- **Severities**: Critical, High, Medium
- **States**: Urgent, Confirmed, To-verify
- **Status**: New, Recurrent

### Command Line Arguments

The script accepts the following command line arguments:

- **scan_id** (required): The UUID of the scan to generate a report for

You can get scan IDs from your Checkmarx AST dashboard or by using the projects API endpoint.

## API Endpoints

The tool utilizes the following Checkmarx API endpoints:

- **Authentication**: `/auth/realms/{tenant}/protocol/openid-connect/token`
- **Projects**: `/projects/last-scan`
- **Reports**: `/reports/v2`

## Error Handling

The application includes comprehensive error handling for:

- Configuration file loading errors
- OAuth authentication failures
- API request timeouts and connection issues
- Invalid API responses

All errors are logged with timestamps and detailed error messages.

## Security Considerations

- API keys are treated as sensitive information
- Only the last 8 characters of tokens are logged for debugging
- Configuration files should be excluded from version control
- Use HTTPS endpoints for all API communications

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Verify your API key and tenant name are correct
2. **Network Timeouts**: Check your internet connection and Checkmarx service status
3. **Invalid Scan ID**: Ensure the scan ID exists and you have access permissions
4. **Email Delivery Failed**: Verify email addresses are valid and properly formatted

### Logging

The application logs all operations with timestamps. Check the console output for detailed error messages and debugging information.

## File Structure

```
report-generator/
├── send_report.py          # Main application script
├── utils/
│   └── generate_oauth_token.py  # OAuth authentication utilities
├── config.json             # Configuration file (create from example)
├── example-config.json     # Configuration template
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and development purposes.

## Support

For issues related to:
- Checkmarx API: Contact Checkmarx support
- This tool: Create an issue in this repository