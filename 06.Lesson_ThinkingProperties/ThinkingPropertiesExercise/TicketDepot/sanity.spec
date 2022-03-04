methods {
	owner() returns (address) envfree
	transactionFee() returns (uint64) envfree
	getEventData(uint16) returns (address, uint64, uint16) envfree
	getAttendee(uint16, uint16) returns (address) envfree
	getNumEvents() returns (uint16) envfree

	ticketDepot(uint64)
	createEvent(uint64, uint16) returns (uint16)
	buyNewTicket(uint16, address) returns (uint16)
	offerTicket(uint16, uint16, uint64, address, uint16)
	buyOfferedTicket(uint16, uint16, address)
}

function getEventOwner(uint16 eventID) returns address {
    address owner; uint64 ticketPrice; uint16 ticketsRemaining;
    owner, ticketPrice, ticketsRemaining = getEventData(eventID);
    return owner;
}

function getEventTicketPrice(uint16 eventID) returns uint64 {
    address owner; uint64 ticketPrice; uint16 ticketsRemaining;
    owner, ticketPrice, ticketsRemaining = getEventData(eventID);
    return ticketPrice;
}

function getEventTicketsRemaining(uint16 eventID) returns uint16 {
    address owner; uint64 ticketPrice; uint16 ticketsRemaining;
    owner, ticketPrice, ticketsRemaining = getEventData(eventID);
    return ticketsRemaining;
}

definition isEventCreated(uint16 eventID) returns bool = getEventOwner(eventID) != 0;

// Rule 1
rule eventIsEmptyBeforeCreated(method f, uint16 eventID) {
	env e;
	calldataarg arg;
	f(e, arg);

	uint64 ticketPrice = getEventTicketPrice(eventID);
	uint64 ticketsRemaining = getEventTicketsRemaining(eventID);
	assert !isEventCreated(eventID) => (ticketPrice == 0 && ticketsRemaining == 0);
}

// Rule 2
rule eventOnlyCreatedWithCreateEvent(method f, uint16 eventID) {
	env e;
	calldataarg arg;
	bool eventCreatedBefore = isEventCreated(eventID);
	f(e, arg);
	bool eventCreatedAfter = isEventCreated(eventID);

	assert (!eventCreatedBefore && eventCreatedAfter) => (f.selector == createEvent(uint64, uint16).selector);
}

// Rule 3
rule nonIncreasingTicketsRemaining(method f, uint16 eventID) {
	env e;
	calldataarg arg;
	uint64 ticketRemainingBefore = getEventTicketsRemaining(eventID);
	f(e, arg);
	uint64 ticketRemainingAfter = getEventTicketsRemaining(eventID);

	assert isEventCreated(eventID) => (ticketRemainingBefore >= ticketRemainingAfter);
}

// Rule 4
rule attendeeOnlyChangedWhenBuyOfferedTicket(method f, uint16 eventID, uint16 ticketID) {
	env e;
	calldataarg arg;
	address attendeeBefore = getAttendee(eventID, ticketID);
	f(e, arg);
	address attendeeAfter = getAttendee(eventID, ticketID);

	assert (attendeeBefore != attendeeAfter) => (f.selector == buyOfferedTicket(uint16, uint16, address).selector);
}

// Rule 6
rule monotonicNumEvents(method f) {
	env e;
	calldataarg arg;

	uint16 numEventsBefore = getNumEvents();

	f(e, arg);
	uint16 numEventsAfter = getNumEvents();

	assert numEventsBefore <= numEventsAfter;
}
