methods {
	getStateById(uint256) returns (uint8) envfree
	getStartTimeById(uint256) returns (uint256) envfree
	getEndTimeById(uint256) returns (uint256) envfree
	getNumOfParticipents(uint256) returns (uint256) envfree
    getOrganizer(uint256) returns (address) envfree
}

// Meeting status in MeetingScheduler
definition UNINITIALIZED() returns uint8 = 0;
definition PENDING() returns uint8 = 1;
definition STARTED() returns uint8 = 2;
definition ENDED() returns uint8 = 3;
definition CANCELLED() returns uint8 = 4;


// ### Valid State
// 1. (state = UNINITIALIZED) => all fields in ScheduledMeeting shall be empty.
rule meetingIsEmptyWhenUnitialized(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    // Precondition is required to avoid wrong initial values.
    require (
        getStateById(meetingId) == UNINITIALIZED() &&
        getStartTimeById(meetingId) == 0 &&
        getEndTimeById(meetingId) == 0 &&
        getNumOfParticipents(meetingId) == 0 &&
        getOrganizer(meetingId) == 0
    );
	f(e, args);
    assert (getStateById(meetingId) == UNINITIALIZED()) => (
        getStartTimeById(meetingId) == 0 &&
        getEndTimeById(meetingId) == 0 &&
        getNumOfParticipents(meetingId) == 0 &&
        getOrganizer(meetingId) == 0
    );
}


// ### State Transitions
// 2. (beforeState = PENDING and afterState = STARTED) => f.selector = startMeeting(uint256)
rule startedOnlyWhenStartMeeting(method f, uint256 meetingId) {
	env e;
	calldataarg args;

    uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
    assert (stateBefore == PENDING() && stateAfter == STARTED()) => (f.selector == startMeeting(uint256).selector);
}

// ### Variable Transitions
// 3. ScheduledMeeting.organizer can only be set by scheduleMeeting.
rule organizerCanOnlyBeSetWhenStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;

    address organizerBefore = getOrganizer(meetingId);
	f(e, args);
    address organizerAfter = getOrganizer(meetingId);

    assert (organizerBefore != organizerAfter) => (f.selector == scheduleMeeting(uint256, uint256, uint256).selector);
}

// ### High-Level Properties
// 4. For a meeting, except for scheduleMeeting, startTime and endTime must not be changed.
rule organizerCanOnlySetWhenStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;

    uint256 startTimeBefore = getStartTimeById(meetingId);
    uint256 endTimeBefore = getEndTimeById(meetingId);
	f(e, args);
    uint256 startTimeAfter = getStartTimeById(meetingId);
    uint256 endTimeAfter = getEndTimeById(meetingId);

    assert (startTimeBefore != startTimeAfter || endTimeBefore != endTimeAfter) => (f.selector == scheduleMeeting(uint256, uint256, uint256).selector);
}

// ### Unit Tests
// 5. After joinMeeting is called, numOfParticipants is increased by 1.
rule testJoinMeeting(uint256 meetingId) {
	env e;
    uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);
    joinMeeting(e, meetingId);
    uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

    assert (numOfParticipantsAfter == numOfParticipantsBefore + 1);
}
