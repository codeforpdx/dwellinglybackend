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


def test_notes():
    """The properties must match the notes model's inputs."""

    testTicketId = 1
    testText = 'Tenant has 40 cats'
    testUserId = 1

    test_note = NotesModel(
        ticketid=testTicketId,
        text=testText,
        userid=testUserId,
    )

    assert test_note.ticketid == testTicketId
    assert test_note.text == testText
    assert test_note.userid == testUserId
