import gixy
from gixy.plugins.plugin import Plugin

class hash_without_default(Plugin):
    summary = "Detect when a hash block (map, geo) is used without a default value."
    severity = gixy.severity.MEDIUM
    description = "A hash block without a default value may allow the bypassing of security controls."
    help_url = "https://joshua.hu/todo"
    directives = ["map", "geo"]

    def __init__(self, config):
        super(hash_without_default, self).__init__(config)

    def audit(self, directive):
        found_default = False
        for child in directive.children:
            if child.src_val == 'default' and child.dest_val is not None:
                found_default = True
                break
        if not found_default:
            self.add_issue(directive=[directive] + directive.children, reason="Missing default value in {0} ${1}".format(directive.name, directive.variable))
