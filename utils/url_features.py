import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = {
    'login', 'verify', 'update', 'secure', 'account', 'bank', 'wallet', 'otp',
    'signin', 'payment', 'confirm', 'unlock', 'reset', 'suspend', 'alert'
}

SHORTENERS = {'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'ow.ly', 'buff.ly', 'cutt.ly'}
SUSPICIOUS_TLDS = {'.ru', '.tk', '.xyz', '.top', '.gq', '.ml', '.cf'}
TRUSTED_BRANDS = {'paypal', 'amazon', 'microsoft', 'google', 'apple', 'bank', 'netflix'}


def _has_ip_address(hostname: str) -> bool:
    if not hostname:
        return False
    ip_pattern = r'^(?:\d{1,3}\.){3}\d{1,3}$'
    return bool(re.match(ip_pattern, hostname))


def extract_url_features(url: str):
    working_url = url.strip()
    if not working_url.startswith(('http://', 'https://')):
        working_url = 'http://' + working_url

    parsed = urlparse(working_url)
    hostname = (parsed.netloc or '').split('@')[-1].split(':')[0].lower()
    path = (parsed.path or '').lower()
    full = working_url.lower()

    dot_count = hostname.count('.')
    url_length = len(working_url)
    has_at_symbol = '@' in working_url
    has_hyphen = '-' in hostname
    uses_https = parsed.scheme == 'https'
    uses_shortener = hostname in SHORTENERS
    has_ip = _has_ip_address(hostname)
    suspicious_keyword_hits = [kw for kw in SUSPICIOUS_KEYWORDS if kw in full]
    tld_hit = next((tld for tld in SUSPICIOUS_TLDS if hostname.endswith(tld)), None)

    brand_mismatch = False
    for brand in TRUSTED_BRANDS:
        if brand in full and brand not in hostname:
            brand_mismatch = True
            break

    feature_map = {
        'url_length': url_length,
        'subdomain_depth': max(dot_count - 1, 0),
        'has_at_symbol': int(has_at_symbol),
        'has_hyphen': int(has_hyphen),
        'uses_https': int(uses_https),
        'uses_shortener': int(uses_shortener),
        'has_ip_address': int(has_ip),
        'keyword_hits': len(suspicious_keyword_hits),
        'suspicious_tld': int(bool(tld_hit)),
        'brand_mismatch': int(brand_mismatch),
        'path_length': len(path),
    }

    reasons = []
    if url_length > 75:
        reasons.append('URL is unusually long.')
    if feature_map['subdomain_depth'] >= 2:
        reasons.append('URL contains multiple subdomain levels.')
    if has_at_symbol:
        reasons.append('URL contains @ symbol, which can obscure the real destination.')
    if has_hyphen:
        reasons.append('Domain contains a hyphen, often used in deceptive domains.')
    if not uses_https:
        reasons.append('URL does not use HTTPS.')
    if uses_shortener:
        reasons.append('URL uses a shortening service.')
    if has_ip:
        reasons.append('URL uses an IP address instead of a domain name.')
    if suspicious_keyword_hits:
        reasons.append('Suspicious keywords found: ' + ', '.join(sorted(set(suspicious_keyword_hits))) + '.')
    if tld_hit:
        reasons.append(f'Domain ends with a high-risk TLD ({tld_hit}).')
    if brand_mismatch:
        reasons.append('Brand-like keyword appears in the URL but not in the actual hostname.')

    return feature_map, reasons, working_url
