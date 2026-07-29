from aidk.audit.command import AuditCommand


def test_audit_command():

    cmd = AuditCommand()

    assert cmd.run() == 0
