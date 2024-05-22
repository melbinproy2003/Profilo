from urllib.parse import urlparse

SOCIAL_MEDIA_DOMAINS = {
    "facebook": ["facebook.com", "fb.com"],
    "twitter": ["twitter.com", "t.co"],
    "instagram": ["instagram.com", "instagr.am"],
    "linkedin": ["linkedin.com", "lnkd.in"],
    "youtube": ["youtube.com", "youtu.be"],
    "pinterest": ["pinterest.com", "pin.it"],
    "tiktok": ["tiktok.com"],
    "github": ["github.com"],
}

def get_domain_from_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Assume http if no scheme is provided
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception as e:
        return None

def identify_social_media_platform(url):
    domain = get_domain_from_url(url)
    if domain:
        for platform, domains in SOCIAL_MEDIA_DOMAINS.items():
            if domain in domains:
                return platform
    return "globe"
