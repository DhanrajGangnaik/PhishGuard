import re

URGENT_WORDS = {
    'urgent', 'immediately', 'verify', 'suspend', 'click below', 'limited time',
    'action required', 'update now', 'confirm now', 'security alert', 'reset now'
}

CREDENTIAL_WORDS = {
    'password', 'otp', 'pin', 'cvv', 'credit card', 'bank details', 'login details', 'account credentials'
}

AUTHORITY_WORDS = {
    'bank', 'support team', 'it admin', 'microsoft', 'google', 'paypal', 'security team', 'administrator'
}


def extract_email_features(text: str):
    clean = text.strip().lower()
    urls = re.findall(r'https?://\S+|www\.\S+', clean)
    exclamations = clean.count('!')

    urgent_hits = [w for w in URGENT_WORDS if w in clean]
    credential_hits = [w for w in CREDENTIAL_WORDS if w in clean]
    authority_hits = [w for w in AUTHORITY_WORDS if w in clean]

    feature_map = {
        'text_length': len(clean),
        'url_count': len(urls),
        'urgent_hits': len(urgent_hits),
        'credential_hits': len(credential_hits),
        'authority_hits': len(authority_hits),
        'exclamation_count': exclamations,
        'contains_attachment_lure': int(any(x in clean for x in ['attachment', 'invoice', 'document', 'open file'])),
        'contains_reward_lure': int(any(x in clean for x in ['won', 'reward', 'gift', 'prize', 'claim now'])),
    }

    reasons = []
    if urls:
        reasons.append(f'Email contains {len(urls)} embedded link(s).')
    if urgent_hits:
        reasons.append('Urgent language detected: ' + ', '.join(sorted(set(urgent_hits))) + '.')
    if credential_hits:
        reasons.append('Message requests sensitive information: ' + ', '.join(sorted(set(credential_hits))) + '.')
    if authority_hits:
        reasons.append('Message imitates an authority or trusted brand: ' + ', '.join(sorted(set(authority_hits))) + '.')
    if exclamations >= 3:
        reasons.append('Message uses excessive punctuation to create pressure.')
    if feature_map['contains_attachment_lure']:
        reasons.append('Attachment or invoice lure detected.')
    if feature_map['contains_reward_lure']:
        reasons.append('Reward or prize lure detected.')

    return feature_map, reasons
