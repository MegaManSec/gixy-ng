import gixy
from gixy.plugins.plugin import Plugin


class version_disclosure(Plugin):
    """
    Syntax for the directive: server_tokens off;
    """
    summary = 'Do not enable server_tokens on or server_tokens build'
    severity = gixy.severity.HIGH
    description = ("Using server_tokens on; or server_tokens build;  allows an "
                   "attacker to learn the version of NGINX you are running, which can "
                   "be used to exploit known vulnerabilities.")
    help_url = 'https://gixy.getpagespeed.com/en/plugins/version_disclosure/'
    directives = ['server_tokens']

    def audit(self, directive):
        if directive.args[0] in ['on', 'build']:
            self.add_issue(
                severity=gixy.severity.HIGH,
                directive=[directive, directive.parent],
                reason="Using server_tokens value which promotes information disclosure"
            )
