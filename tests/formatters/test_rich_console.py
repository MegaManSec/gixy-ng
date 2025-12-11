"""Tests for the Rich console formatter."""

import pytest

# Skip all tests in this module if rich is not installed
pytest.importorskip("rich", reason="rich library required for rich_console formatter tests")


def test_rich_console_formatter_available():
    """Test that rich_console formatter is available."""
    from gixy.formatters import get_all
    formatters = get_all()
    assert 'rich_console' in formatters


def test_rich_console_formatter_produces_output():
    """Test that rich_console formatter produces beautiful output."""
    from gixy.formatters import get_all
    
    formatter_cls = get_all()['rich_console']
    formatter = formatter_cls()
    
    # Create mock reports with an issue
    reports = {
        '/test/nginx.conf': [
            {
                'plugin': 'test_plugin',
                'summary': 'Test issue summary',
                'severity': 'HIGH',
                'description': 'Test description',
                'help_url': 'https://example.com',
                'reason': 'Test reason',
                'config': 'server { test; }',
            }
        ]
    }
    stats = {'HIGH': 1, 'MEDIUM': 0, 'LOW': 0, 'UNSPECIFIED': 0}
    
    output = formatter.format_reports(reports, stats)
    
    # Check output contains expected elements
    assert 'GIXY' in output
    assert 'Security Scanner' in output
    assert 'test_plugin' in output
    assert 'Test issue summary' in output
    assert 'Score' in output
    assert 'Summary' in output
    assert 'CRITICAL' in output  # HIGH severity shown as CRITICAL


def test_rich_console_formatter_no_issues():
    """Test formatter output when no issues are found."""
    from gixy.formatters import get_all
    
    formatter_cls = get_all()['rich_console']
    formatter = formatter_cls()
    
    reports = {'/test/nginx.conf': []}
    stats = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'UNSPECIFIED': 0}
    
    output = formatter.format_reports(reports, stats)
    
    assert 'No security issues found' in output
    assert '100/100' in output
    assert 'EXCELLENT' in output
    assert 'No issues' in output


def test_rich_console_formatter_security_score_calculation():
    """Test that security score is calculated correctly."""
    from gixy.formatters import get_all
    
    formatter_cls = get_all()['rich_console']
    formatter = formatter_cls()
    
    # 3 HIGH issues = 75 points deducted, score = 25
    reports = {'/test/nginx.conf': [
        {'plugin': 'p1', 'summary': 's1', 'severity': 'HIGH', 'description': '', 'help_url': '', 'reason': '', 'config': ''},
        {'plugin': 'p2', 'summary': 's2', 'severity': 'HIGH', 'description': '', 'help_url': '', 'reason': '', 'config': ''},
        {'plugin': 'p3', 'summary': 's3', 'severity': 'HIGH', 'description': '', 'help_url': '', 'reason': '', 'config': ''},
    ]}
    stats = {'HIGH': 3, 'MEDIUM': 0, 'LOW': 0, 'UNSPECIFIED': 0}
    
    output = formatter.format_reports(reports, stats)
    
    # Score should be 25 (100 - 3*25)
    assert '25/100' in output
    assert 'CRITICAL' in output  # Low score = CRITICAL rating


def test_rich_console_formatter_different_severities():
    """Test formatter handles all severity levels."""
    from gixy.formatters import get_all
    
    formatter_cls = get_all()['rich_console']
    formatter = formatter_cls()
    
    reports = {'/test/nginx.conf': [
        {'plugin': 'p1', 'summary': 'High issue', 'severity': 'HIGH', 'description': '', 'help_url': '', 'reason': '', 'config': ''},
        {'plugin': 'p2', 'summary': 'Medium issue', 'severity': 'MEDIUM', 'description': '', 'help_url': '', 'reason': '', 'config': ''},
        {'plugin': 'p3', 'summary': 'Low issue', 'severity': 'LOW', 'description': '', 'help_url': '', 'reason': '', 'config': ''},
    ]}
    stats = {'HIGH': 1, 'MEDIUM': 1, 'LOW': 1, 'UNSPECIFIED': 0}
    
    output = formatter.format_reports(reports, stats)
    
    # All severity labels should appear in issue panels
    assert 'CRITICAL' in output  # HIGH
    assert 'WARNING' in output   # MEDIUM
    assert 'INFO' in output      # LOW
    # Summary should show total
    assert '3 total' in output


def test_rich_console_formatter_shows_line_numbers():
    """Test formatter displays file and line number information."""
    from gixy.formatters import get_all
    
    formatter_cls = get_all()['rich_console']
    formatter = formatter_cls()
    
    reports = {'/etc/nginx/nginx.conf': [
        {
            'plugin': 'test_plugin',
            'summary': 'Test issue',
            'severity': 'HIGH',
            'description': 'Test description',
            'help_url': '',
            'reason': 'Test reason',
            'config': 'server_tokens on;',
            'location': {'file': '/etc/nginx/nginx.conf', 'line': 42},
        }
    ]}
    stats = {'HIGH': 1, 'MEDIUM': 0, 'LOW': 0, 'UNSPECIFIED': 0}
    
    output = formatter.format_reports(reports, stats)
    
    # Should show file:line in VSCode-compatible format
    assert '/etc/nginx/nginx.conf:42' in output

