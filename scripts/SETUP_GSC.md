# Google Search Console Setup for dyarnaa.com

This guide explains how to enable the optional Search Console API integration
in `indexing_monitor.py`. Without this setup, the monitor runs with local
checks only (sitemap, HTTP status, canonical, robots meta).

## Option A: Domain Property (Recommended)

A **Domain property** covers all protocols and subdomains (`http://`, `https://`,
`www`, non-`www`). It requires DNS verification.

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Click **Add property** → **Domain**
3. Enter `dyarnaa.com`
4. Google gives you a DNS TXT record to add:
   ```
   Name: @ (or blank, for the root domain)
   Type: TXT
   Value: <google-given-token>
   ```
5. Add this TXT record to the dyarnaa.com DNS zone.
6. Once DNS propagates (use `dig TXT dyarnaa.com` or online tools), click
   **Verify** in Search Console.

## Option B: URL-Prefix Property

If DNS management is not possible, use a URL-prefix property:

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Click **Add property** → **URL prefix**
3. Enter `https://dyarnaa.com/`
4. Choose an existing verification method (DNS TXT, HTML file, Google Analytics,
   or Google Tag Manager).
5. For HTML file verification: download the HTML file and upload it to the
   site's root (`dist/` in the Astro project), then commit & push.

## Creating a Service Account for API Access

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create the project used by the site
3. Go to **IAM & Admin → Service Accounts**
4. Click **Create Service Account**
5. Name: `diarna-indexing-monitor`
6. Grant this service account **Search Console User** access:
   - Go to the Google Search Console property → **Settings → Owners & users**
   - Add the service account's email (e.g., `diarna-indexing-monitor@your-project.iam.gserviceaccount.com`)
   - Role: **Full** or **Restricted** (restricted is sufficient for read + sitemap submit)
7. Download the JSON key file
8. Save it to: `/opt/data/secrets/gsc-service-account.json` (chmod 600)
   OR set the `GSC_SERVICE_ACCOUNT` environment variable to the file path

## Enabling Search Console API

1. In Google Cloud Console, go to **APIs & Services → Library**
2. Search for **Google Search Console API**
3. Click **Enable**

## Verifying Access

After setup, run:
```bash
python3 /opt/data/projects/diarna-stone/scripts/indexing_monitor.py --summary
```

When GSC is available, the report will show `"gsc": {"available": true, ...}`.

## Manual Checks (while GSC is not set up)

These can be done manually in Search Console without the API:

- **URL Inspection**: Paste key URLs (homepage, product pages, blog posts) into
  the URL Inspection tool at https://search.google.com/search-console/inspect
- **Sitemaps**: Go to **Sitemaps** in the left menu to submit `sitemap.xml`
  and monitor indexing status
- **Coverage**: Go to **Coverage** to see indexed vs. excluded URLs and reasons
