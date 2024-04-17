from ipaddress import IPv4Network, AddressValueError
from dns import resolver
from app import env


def pretty_print(data, **kwargs):
    print("\033[92m{}\033[00m".format(data), **kwargs)


def error_resp(message):
    return {
        'status': 'error',
        'message': message
    }


def success_resp(message):
    return {
        'status': 'success',
        'message': message
    }


def validate_scan_job(ip_block: str) -> str | None:
    """
    Validates the IP block w/o CIDR or FQDN
    Args:
        ip_block: IP/IP block/ FQDN
    Returns:
        IP Block in CIDR notation if valid
        None if invalid
    """
    try:
        ip_block = IPv4Network(ip_block, strict=False)  # will raise AddressValueError if not a valid IP
    except AddressValueError:  # if not a valid IP, try to resolve it
        try:
            ip_block = env.resolver.query(ip_block, 'A')[0].to_text()
        except resolver.NXDOMAIN:  # if not a valid FQDN, return error
            return None
    except Exception as e:
        print(f"Error validating scan job: {e}")
        return None
    return str(ip_block)


def resolve_ip_block(ip_block: str) -> list | None:
    """
    Resolves an IP block to a list of IPs
    Args:
        ip_block: str: IP block in CIDR notation
    Returns:
        list: List of IPs in the block
        None: if the block is invalid
    """
    try:
        return [str(ip) for ip in IPv4Network(ip_block)]
    except ValueError:
        return None
