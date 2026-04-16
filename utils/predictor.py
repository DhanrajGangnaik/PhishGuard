from utils.url_features import extract_url_features
from utils.email_features import extract_email_features


def _score_to_label(score: int) -> str:
    if score >= 61:
        return 'Phishing'
    if score >= 31:
        return 'Suspicious'
    return 'Safe'


def analyze_url(content: str):
    feature_map, reasons, normalized = extract_url_features(content)

    score = 0
    score += 20 if feature_map['has_ip_address'] else 0
    score += 12 if feature_map['uses_shortener'] else 0
    score += 12 if feature_map['has_at_symbol'] else 0
    score += 8 if feature_map['has_hyphen'] else 0
    score += 10 if not feature_map['uses_https'] else 0
    score += 10 if feature_map['suspicious_tld'] else 0
    score += 12 if feature_map['brand_mismatch'] else 0
    score += min(feature_map['keyword_hits'] * 7, 21)
    score += 8 if feature_map['subdomain_depth'] >= 2 else 0
    score += 8 if feature_map['url_length'] > 75 else 0

    score = min(score, 100)
    label = _score_to_label(score)

    if not reasons and label == 'Safe':
        reasons = ['No major phishing indicators were detected.']

    return {
        'input_type': 'URL',
        'content': normalized,
        'label': label,
        'score': score,
        'reasons': reasons,
        'features': feature_map,
    }



def analyze_email(content: str):
    feature_map, reasons = extract_email_features(content)

    score = 0
    score += min(feature_map['urgent_hits'] * 12, 24)
    score += min(feature_map['credential_hits'] * 15, 30)
    score += min(feature_map['authority_hits'] * 8, 16)
    score += min(feature_map['url_count'] * 10, 20)
    score += 8 if feature_map['contains_attachment_lure'] else 0
    score += 8 if feature_map['contains_reward_lure'] else 0
    score += 6 if feature_map['exclamation_count'] >= 3 else 0

    score = min(score, 100)
    label = _score_to_label(score)

    if not reasons and label == 'Safe':
        reasons = ['No major phishing indicators were detected.']

    return {
        'input_type': 'Email',
        'content': content,
        'label': label,
        'score': score,
        'reasons': reasons,
        'features': feature_map,
    }



def analyze_input(input_type: str, content: str):
    if input_type == 'email':
        return analyze_email(content)
    return analyze_url(content)
