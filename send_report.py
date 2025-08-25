
#Standard Library
import argparse
import logging
import sys
#Third-party
import requests
#Local
from utils.generate_oauth_token import load_config, generate_oauth_token


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# Load configuration from config.json
CONFIG = load_config()
BASE_API_URL = CONFIG.get("api_url")
REQUEST_TIMEOUT = 10  # seconds

if not BASE_API_URL:
    sys.exit("api_url missing in config.json")

# Get a dict of projects from the API
def get_projects(token: str,headers: dict) -> dict:
    """Return a dict of projects (or an empty dict on failure)."""
    url = f"{BASE_API_URL}/projects/last-scan"
    #Example for Params
    params = {
        "limit": 10,  # Example parameter to limit the number of projects returned
    }
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT,params=params)
        response.raise_for_status()
        return response.json().get("projects", [])
    except requests.RequestException as err:
        log.error(f"Project request failed: {err}")
        return {}

def create_customized_report(headers: dict, scan_id: str) -> dict:
    """
    Create an improved scan report using POST /reports/v2.
    Follows Checkmarx schema for Scan reports.
    """
    url = f"{BASE_API_URL}/reports/v2"

    data = {
        # Required
        "reportName": "improved-scan-report",   # must be this exact string
        "reportType": "email",                  # "cli", "ui", "email"
        "fileFormat": "pdf",                    # "pdf", "json", "csv"

        # Optional
        "reportFilename": "",                   # server defaults if empty
        "sections": [
            "scan-information",
            "results-overview",
            "scan-results",
            "resolved-results",
            "categories",
            "vulnerability-details"
        ],

        # Only required if reportType = "email"
        "emails": CONFIG.get("email_to") if isinstance(CONFIG.get("email_to"), list) else [CONFIG.get("email_to")],

        # Entities block — for improved-scan-report, must be scan
        "entities": [
            {
                "entity": "scan",
                "ids": [scan_id]   # only one scanId allowed
            }
        ],

        # Filters (all optional, defaults kick in if omitted)
        "filters": {
            "scanners": ["sast", "sca", "iac", "containers", "microengines"],
            "severities": ["critical", "high", "medium"],    # default set
            "states": ["urgent", "confirmed", "to-verify"],  # default set
            "status": ["new", "recurrent"]                   # default = all
        }
    }

    try:
        response = requests.post(url, headers=headers, timeout=REQUEST_TIMEOUT, json=data)
        response.raise_for_status()
        log.info(f"Customized scan report requested; response: {response.json()}")
        return response.json()
    except requests.RequestException as err:
        log.error(f"Customized scan report creation failed: {err}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Generate and send Checkmarx security scan reports")
    parser.add_argument("scan_id", help="The scan ID to generate a report for")
    
    args = parser.parse_args()
    
    token = generate_oauth_token(CONFIG)
    if not token:
        log.error("Could not obtain OAuth token.")
        return

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    log.info(f"OAuth token obtained: ***{token[-8:]}")  # Log only the last 8 characters for security
    log.info(f"Generating report for scan ID: {args.scan_id}")
    
    response = create_customized_report(headers, args.scan_id)
    log.info(f"Report creation response: {response}")

if __name__ == "__main__":
    main()
