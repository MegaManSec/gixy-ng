import re
import gixy
import sys
from gixy.plugins.plugin import Plugin

class proxy_pass_normalized(Plugin):
    r"""
    This plugin detects if there is any path component (slash or more)
    after the host in a proxy_pass directive.
    Example flagged directives:
        proxy_pass http://backend/;
        proxy_pass http://backend/foo/bar;
    """

    summary = 'Detect path after host in proxy_pass (potential URL decoding issue)'
    severity = gixy.severity.MEDIUM
    description = ("A path (beginning with a slash) after the host in proxy_pass leads to the path being decoded and normalized before proxying downstream, leading to unexpected behavior related to encoded slashes like %2F..%2F. Likewise, the usage of 'rewrite ^ $request_uri;' without using '$1' or '$uri' (or another captured group) in the path of proxy_pass leads to double-encoding of paths.")
    help_url = 'https://joshua.hu/proxy-pass-nginx-decoding-normalizing-url-path-dangerous#nginx-proxy_pass'
    directives = ['proxy_pass']

    def __init__(self, config):
        super(proxy_pass_normalized, self).__init__(config)
        self.parse_uri_re = re.compile(r'(?P<scheme>[^?#/)]+://)?(?P<host>[^?#/)]+)(?P<path>/.*)?')

    def audit(self, directive):
        proxy_pass_args = directive.args
        rewrite_fail = False
        num_pattern = r'\$\d+'

        if not proxy_pass_args:
            return

        parsed = self.parse_uri_re.match(proxy_pass_args[0])

        if not parsed:
            return

        for rewrite in directive.find_directives_in_scope("rewrite"):
            if hasattr(rewrite, 'pattern') and hasattr(rewrite, 'replace'):
                if rewrite.pattern == '^' and rewrite.replace == '$request_uri':
                    if parsed.group('path'):
                        match = re.search(num_pattern, parsed.group('path'))
                        if match or '$uri' in parsed.group('path'):
                            return
                        else:
                            rewrite_fail = True
                            break
                    else:
                        if not parsed.group('host'):
                            return # ?!
                        match = re.search(num_pattern, parsed.group('host'))
                        if match or '$uri' in parsed.group('host'):
                            return
                        else:
                            rewrite_fail = True
                            break

        if not parsed.group('path') and not rewrite_fail:
            return

        self.add_issue(
            severity=self.severity,
            directive=[directive, directive.parent],
            reason=(
                "Found a path after the host in proxy_pass, without using $request_uri and a variable (such as $1 or $uri). "
                "This can lead to path decoding issues or double-encoding issues."
            )
        )
