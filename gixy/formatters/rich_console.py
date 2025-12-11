"""
🔥 GIXY Rich Console Formatter 🔥

A stunning terminal UI that makes security analysis beautiful.
Optional: requires `rich` library. Install with: pip install gixy-ng[rich]
"""

from __future__ import absolute_import

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.text import Text
    from rich.syntax import Syntax
    from rich.box import ROUNDED, DOUBLE
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Only define the formatter class if Rich is available
# This prevents it from appearing in --help when Rich isn't installed
if RICH_AVAILABLE:
    import gixy
    from gixy.formatters.base import BaseFormatter

    # Severity styling configuration
    SEVERITY_STYLES = {
        'HIGH': {
            'color': 'red',
            'icon': '🔴',
            'label': 'CRITICAL',
            'border': 'red',
            'score_weight': 25,
        },
        'MEDIUM': {
            'color': 'yellow',
            'icon': '🟠',
            'label': 'WARNING',
            'border': 'yellow',
            'score_weight': 10,
        },
        'LOW': {
            'color': 'blue',
            'icon': '🔵',
            'label': 'INFO',
            'border': 'blue',
            'score_weight': 3,
        },
        'UNSPECIFIED': {
            'color': 'dim',
            'icon': '⚪',
            'label': 'NOTE',
            'border': 'dim',
            'score_weight': 1,
        },
    }

    class Rich_consoleFormatter(BaseFormatter):
        """Beautiful Rich-based terminal formatter for gixy output."""

        def __init__(self):
            super(Rich_consoleFormatter, self).__init__()
            self.console = Console(force_terminal=True)

        def format_reports(self, reports, stats):
            """Format all reports into a stunning terminal output."""
            from io import StringIO
            string_buffer = StringIO()
            buffer_console = Console(file=string_buffer, force_terminal=True, width=100)

            # Header
            self._render_header(buffer_console)

            # Process each file's reports
            for path, issues in reports.items():
                if len(reports) > 1:
                    self._render_file_header(buffer_console, path)

                if not issues:
                    self._render_no_issues(buffer_console)
                else:
                    # Sort by severity (HIGH first)
                    severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'UNSPECIFIED': 3}
                    sorted_issues = sorted(issues, key=lambda x: severity_order.get(x['severity'], 4))

                    for i, issue in enumerate(sorted_issues):
                        self._render_issue(buffer_console, issue, i + 1, len(sorted_issues))

            # Security Score
            self._render_security_score(buffer_console, stats)

            # Summary
            self._render_summary(buffer_console, stats)

            # Footer
            self._render_footer(buffer_console)

            return string_buffer.getvalue()

        def _render_header(self, console):
            """Render the awesome header."""
            header_text = Text()
            header_text.append("🛡️  ", style="bold")
            header_text.append("GIXY", style="bold magenta")
            header_text.append(" Security Scanner", style="bold white")
            header_text.append(f"  v{gixy.version}", style="dim")

            console.print(Panel(
                header_text,
                box=DOUBLE,
                style="magenta",
                padding=(0, 2),
            ))

        def _render_file_header(self, console, path):
            """Render file path header."""
            console.print(
                Panel(
                    f"📁 [bold]{path}[/bold]",
                    box=ROUNDED,
                    style="cyan",
                    padding=(0, 1),
                )
            )

        def _render_no_issues(self, console):
            """Render the happy no-issues message."""
            console.print(Panel(
                Text.from_markup(
                    "[bold green]✅ No security issues found![/bold green]\n"
                    "[dim]Your NGINX configuration looks secure.[/dim]"
                ),
                box=ROUNDED,
                style="green",
                padding=(0, 2),
            ))

        def _render_issue(self, console, issue, index, total):
            """Render a single issue with all its glory."""
            severity = issue['severity']
            style = SEVERITY_STYLES.get(severity, SEVERITY_STYLES['UNSPECIFIED'])

            # Issue header
            header = Text()
            header.append(f"{style['icon']} ", style="bold")
            header.append(f"{style['label']}", style=f"bold {style['color']}")
            header.append(" │ ", style="dim")
            header.append(f"[{issue['plugin']}]", style="bold white")
            header.append(f" {issue['summary']}", style="white")

            # Build content
            content_parts = []

            # Location (file:line) - VSCode-compatible format for click-to-jump
            location = issue.get('location')
            if location and location.get('line'):
                loc_text = Text()
                loc_text.append("📍 ", style="dim")
                if location.get('file'):
                    loc_text.append(f"{location['file']}:{location['line']}", style="cyan underline")
                else:
                    loc_text.append(f":{location['line']}", style="cyan")
                content_parts.append(loc_text)

            # Description
            if issue.get('description'):
                content_parts.append(
                    Text.from_markup(f"[dim]{issue['description']}[/dim]")
                )

            # Reason
            if issue.get('reason'):
                reason_text = Text()
                reason_text.append("💡 ", style="bold cyan")
                reason_text.append(issue['reason'], style="white")
                content_parts.append(reason_text)

            # Config snippet
            if issue.get('config'):
                config_syntax = Syntax(
                    issue['config'],
                    "nginx",
                    theme="monokai",
                    line_numbers=False,
                    word_wrap=True,
                    background_color="default",
                )
                content_parts.append(config_syntax)

            # Help URL
            if issue.get('help_url'):
                link_text = Text()
                link_text.append("📚 ", style="dim")
                link_text.append(issue['help_url'], style="underline blue dim")
                content_parts.append(link_text)

            # Combine all content
            panel_content = Group(*content_parts)

            # Create the panel
            console.print(Panel(
                panel_content,
                title=header,
                title_align="left",
                box=ROUNDED,
                border_style=style['border'],
                padding=(0, 1),
            ))

        def _render_security_score(self, console, stats):
            """Render an awesome security score visualization."""
            total_deduction = 0
            for severity, count in stats.items():
                weight = SEVERITY_STYLES.get(severity, {}).get('score_weight', 1)
                total_deduction += count * weight

            score = max(0, 100 - total_deduction)

            # Determine score color and message
            if score >= 90:
                score_color = "green"
                score_icon = "🏆"
                score_label = "EXCELLENT"
            elif score >= 70:
                score_color = "yellow"
                score_icon = "👍"
                score_label = "GOOD"
            elif score >= 50:
                score_color = "orange1"
                score_icon = "⚠️"
                score_label = "NEEDS WORK"
            else:
                score_color = "red"
                score_icon = "🚨"
                score_label = "CRITICAL"

            # Build the score bar
            bar_width = 40
            filled = int((score / 100) * bar_width)
            empty = bar_width - filled

            score_bar = Text()
            score_bar.append("█" * filled, style=f"bold {score_color}")
            score_bar.append("░" * empty, style="dim")
            score_bar.append(f"  {score}/100", style=f"bold {score_color}")
            score_bar.append(f"  {score_icon} {score_label}", style=f"bold {score_color}")

            console.print(Panel(
                score_bar,
                title="[bold]📊 Score[/bold]",
                title_align="left",
                box=ROUNDED,
                border_style=score_color,
                padding=(0, 1),
            ))

        def _render_summary(self, console, stats):
            """Render the summary as a compact line."""
            parts = []
            total = 0
            for severity in ['HIGH', 'MEDIUM', 'LOW', 'UNSPECIFIED']:
                count = stats.get(severity, 0)
                total += count
                if count > 0:
                    style_info = SEVERITY_STYLES.get(severity, {})
                    icon = style_info.get('icon', '•')
                    color = style_info.get('color', 'white')
                    parts.append(f"[{color}]{icon} {count}[/{color}]")

            if parts:
                summary_text = Text.from_markup("  ".join(parts) + f"  [dim]│[/dim]  [bold]{total} total[/bold]")
            else:
                summary_text = Text.from_markup("[green]No issues[/green]")

            console.print(Panel(
                summary_text,
                title="[bold]📋 Summary[/bold]",
                title_align="left",
                box=ROUNDED,
                border_style="cyan",
                padding=(0, 1),
            ))

        def _render_footer(self, console):
            """Render the footer with tips."""
            console.print(Text.from_markup(
                "[dim]💡 Keep NGINX secure with [blue underline]nginx-extras.getpagespeed.com[/blue underline][/dim]"
            ), end="")
