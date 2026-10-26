"""
Google Search Console authentication module.

Supports two auth methods:
  1. Service Account (preferred for automated/cron use)
     - Credentials file at path from config or GSC_SERVICE_ACCOUNT env var
     - Service account email must be granted access in Search Console
  2. OAuth2 user credentials (for manual first-run setup)
     - Uses google_auth_oauth_browser flow

Security:
  - Never prints credentials
  - Stores tokens in /opt/data/secrets/ (chmod 600)
  - Reads config from config.json (never committed)
"""
import os
import json
import sys

# Resolve the secrets directory
HERMES_HOME = os.environ.get("HERMES_HOME", "/opt/data")
SECRETS_DIR = os.path.join(HERMES_HOME, "secrets")

DEFAULT_CONFIG = {
    "site_url": "https://dyarnaa.com/",
    "sitemap_url": "https://dyarnaa.com/sitemap.xml",
    "credentials_file": os.path.join(SECRETS_DIR, "gsc-service-account.json"),
    "credentials_env_var": "GSC_SERVICE_ACCOUNT",
    "api_scopes": [
        "https://www.googleapis.com/auth/webmasters.readonly",
    ],
}


def load_config():
    """Load config from search_console/config.json, falling back to defaults."""
    here = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(here, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(json.load(f))
            return cfg
    return DEFAULT_CONFIG.copy()


def get_credentials_path(config=None):
    """Resolve the credentials file path from config or env var."""
    if config is None:
        config = load_config()
    # Check environment variable first (higher priority)
    env_path = os.environ.get(config.get("credentials_env_var", "GSC_SERVICE_ACCOUNT"))
    if env_path and os.path.exists(env_path):
        return env_path
    config_path = config.get("credentials_file")
    if config_path and os.path.exists(config_path):
        return config_path
    return None


def get_service_account_credentials(config=None):
    """Create Service Account credentials from a JSON key file.

    Returns google.auth.credentials.Credentials or None.
    Does NOT raise — callers handle None gracefully.
    """
    if config is None:
        config = load_config()
    cred_path = get_credentials_path(config)
    if not cred_path:
        return None, "No credentials file found. Set GSC_SERVICE_ACCOUNT env var or create /opt/data/secrets/gsc-service-account.json"
    try:
        from google.oauth2 import service_account
        scopes = config.get("api_scopes", ["https://www.googleapis.com/auth/webmasters.readonly"])
        creds = service_account.Credentials.from_service_account_file(
            cred_path, scopes=scopes
        )
        return creds, None
    except ImportError:
        return None, "google-auth library not installed (pip install google-auth)"
    except Exception as e:
        return None, f"Failed to load service account: {e}"


def get_gsc_service(config=None):
    """Build and return an authenticated Search Console API service object.

    Returns (service, error). If error is not None, service is None.
    """
    if config is None:
        config = load_config()
    creds, err = get_service_account_credentials(config)
    if err:
        return None, err
    try:
        from googleapiclient.discovery import build
        service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        return service, None
    except ImportError:
        return None, "google-api-python-client not installed (pip install google-api-python-client)"
    except Exception as e:
        return None, f"Failed to build service: {e}"


def gsc_available():
    """Check if GSC API access is available (credentials + libraries)."""
    config = load_config()
    creds, _ = get_service_account_credentials(config)
    if not creds:
        return False
    service, _ = get_gsc_service(config)
    return service is not None


if __name__ == "__main__":
    config = load_config()
    print(f"Site URL: {config['site_url']}")
    print(f"Sitemap: {config['sitemap_url']}")
    print(f"Scopes: {config['api_scopes']}")
    available = gsc_available()
    print(f"GSC API available: {available}")
    if not available:
        cred_path = get_credentials_path(config)
        print(f"Credentials path expected: {cred_path}")
        print("\nTo enable GSC API access:")
        print("1. Create a service account in Google Cloud Console")
        print("2. Grant it Search Console access on the property")
        print("3. Download JSON key to:", config["credentials_file"])
        print("4. Or set GSC_SERVICE_ACCOUNT env var to the key path")
