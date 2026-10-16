from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_session
from .models import Ticket
from .schemas import TicketInput, TicketOutput, TicketStatus

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

def find_ticket(ticket_id: int, session: Session) -> Ticket:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(404, "Ticket not found")
    return ticket

@router.get("", response_model=list[TicketOutput])
def list_tickets(status: TicketStatus | None = None, session: Session = Depends(get_session)):
    query = select(Ticket).order_by(Ticket.created_at.desc(), Ticket.id.desc())
    if status is not None:
        query = query.where(Ticket.status == status)
    return list(session.scalars(query))

@router.post("", response_model=TicketOutput, status_code=201)
def create_ticket(data: TicketInput, session: Session = Depends(get_session)):
    ticket = Ticket(**data.model_dump())
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.get("/{ticket_id}", response_model=TicketOutput)
def get_ticket(ticket_id: int, session: Session = Depends(get_session)):
    return find_ticket(ticket_id, session)

@router.put("/{ticket_id}", response_model=TicketOutput)
def replace_ticket(ticket_id: int, data: TicketInput, session: Session = Depends(get_session)):
    ticket = find_ticket(ticket_id, session)
    for field, value in data.model_dump().items():
        setattr(ticket, field, value)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, session: Session = Depends(get_session)):
    session.delete(find_ticket(ticket_id, session))
    session.commit()
    return Response(status_code=204)
