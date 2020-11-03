from models.tickets import TicketModel, TicketStatus
from models.notes import NotesModel

def test_ticket():
    """The properties must match the ticket model's inputs."""
    testIssue = 'Property Damage'
    testSender = 'user1 tester'
    testTenant = 'Renty McRenter'
    testStatus = TicketStatus.New
    testUrgency = 'low'
    testAssignedUser = 4

    test_ticket = TicketModel(
        issue=testIssue,
        sender=testSender,
        tenant=testTenant,
        status=testStatus,
        urgency=testUrgency,
        assignedUser=testAssignedUser,
    )

    assert test_ticket.issue == testIssue
    assert test_ticket.sender == testSender
    assert test_ticket.tenant == testTenant
    assert test_ticket.status == testStatus
    assert test_ticket.urgency == testUrgency
    assert test_ticket.assignedUser == testAssignedUser
