import ipaddress

from django.http import Http404


PRIVATE_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]

PROTECTED_PREFIXES = ("/admin/", "/dashboard/", "/auth/")


class LocalNetworkOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(p) for p in PROTECTED_PREFIXES):
            ip = self._get_client_ip(request)
            if not self._is_private(ip):
                raise Http404
        return self.get_response(request)

    def _get_client_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[-1].strip()
        return request.META.get("REMOTE_ADDR", "")

    def _is_private(self, ip_str):
        try:
            addr = ipaddress.ip_address(ip_str)
            return any(addr in net for net in PRIVATE_NETWORKS)
        except ValueError:
            return False
