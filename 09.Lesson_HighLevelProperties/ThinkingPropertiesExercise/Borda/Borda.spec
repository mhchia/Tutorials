methods{
    getPointsOfContender(address) returns(uint256) envfree
    hasVoted(address) returns(bool) envfree
    getWinner() returns(address, uint256) envfree
    getFullVoterDetails(address) returns(uint8, bool, bool, uint256, bool) envfree
    getFullContenderDetails(address) returns(uint8, bool, uint256) envfree
    registerVoter(uint8) returns (bool);
    registerContender(uint8) returns (bool);
    vote(address, address, address) returns (bool);
}


function getVoterReg(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voterReg;
}

function getVoterVoted(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voted;
}

function getVoterVoteAttempts(address voter) returns uint256 {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return vote_attempts;
}

function getVoterBlocked(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;
}

function getContenderAge(address contender) returns uint8 {
    uint8 age; bool isReg; uint256 points;
    age, isReg, points = getFullContenderDetails(contender);
    return age;
}

function getContenderIsReg(address contender) returns bool {
    uint8 age; bool isReg; uint256 points;
    age, isReg, points = getFullContenderDetails(contender);
    return isReg;
}

function getWinnerWinner() returns address {
    address winner; uint256 points;
    winner, points = getWinner();
    return winner;
}

function getWinnerPoints() returns uint256 {
    address winner; uint256 points;
    winner, points = getWinner();
    return points;
}

// unRegisteredVoter - for a voter that isn't registered at all.
definition unRegisteredVoter(address voter) returns bool = (
    !getVoterReg(voter) &&
    !getVoterVoted(voter) &&
    getVoterVoteAttempts(voter) == 0 &&
    !getVoterBlocked(voter)
);
// registeredYetVotedVoter - for a registered voter that hasn't voted yet.
definition registeredYetVotedVoter(address voter) returns bool = (
    getVoterReg(voter) &&
    !getVoterVoted(voter) &&
    getVoterVoteAttempts(voter) == 0 &&
    !getVoterBlocked(voter)
);
// legitRegisteredVotedVoter - for a registered voter that has voted but isn't blocked.
definition legitRegisteredVotedVoter(address voter) returns bool = (
    getVoterReg(voter) &&
    getVoterVoted(voter) &&
    getVoterVoteAttempts(voter) > 0 &&
    getVoterVoteAttempts(voter) < 3 &&
    !getVoterBlocked(voter)
);
// blockedVoter - for a registered voter that has voted, and is blocked.
definition blockedVoter(address voter) returns bool = (
    getVoterReg(voter) &&
    getVoterVoted(voter) &&
    getVoterVoteAttempts(voter) >= 3 &&
    getVoterBlocked(voter)
);

definition nonContender(address a) returns bool = (
    getContenderAge(a) == 0 &&
    !getContenderIsReg(a) &&
    getPointsOfContender(a) == 0
);


// 4.

rule voterRegistered(method f, address voter) {
    env e;
    calldataarg args;

    // FIXME: Strange, this fails...
    // require registeredYetVotedVoter(voter);
    // bool isYetRegistered = registeredYetVotedVoter(voter);
    // Ref: https://prover.certora.com/output/45731/3f2492661dd92c903494/Results.txt?anonymousKey=eda2146b47b91789d75965ffe53848367e485b04
    //  - Message: "java.lang.IllegalStateException: method arg filters in getVoterReg(voter) @ Borda.spec:69:12 may not be null"
    bool isYetRegistered = (
        !getVoterReg(voter) &&
        !getVoterVoted(voter) &&
        getVoterVoteAttempts(voter) == 0 &&
        !getVoterBlocked(voter)
    );
    require isYetRegistered;


    f(e, args);

    bool isRegisteredAfter = getVoterReg(voter);

    assert isRegisteredAfter => (f.selector == registerVoter(uint8).selector);
}


rule voterRegisteredToBlocked(method f, address voter) filtered { f -> !f.isView } {
    env e;
    calldataarg args;

    bool isLegitVotedVoter = (
        getVoterReg(voter) &&
        getVoterVoted(voter) &&
        getVoterVoteAttempts(voter) > 0 &&
        getVoterVoteAttempts(voter) < 3 &&
        !getVoterBlocked(voter)
    );
    require isLegitVotedVoter;

    f(e, args);

    bool isVoterBlocked = (
        getVoterReg(voter) &&
        getVoterVoted(voter) &&
        getVoterVoteAttempts(voter) >= 3 &&
        getVoterBlocked(voter)
    );

    assert isVoterBlocked => f.selector == vote(address, address, address).selector;

}

// 6.
rule pointsIncreased(method f) {
    env e;
    calldataarg args;

    address contender;
    uint256 pointsBefore = getPointsOfContender(contender);

    require getContenderIsReg(contender);

    f(e, args);

    uint256 pointsAfter = getPointsOfContender(contender);

    assert (pointsBefore < pointsAfter) => (f.selector == vote(address, address, address).selector);
}

// 7.
rule pointsCanOnlyBeIncreased(method f) {
    env e;
    calldataarg args;

    address contender;
    uint256 pointsBefore = getPointsOfContender(contender);

    require getContenderIsReg(contender);

    f(e, args);

    uint256 pointsAfter = getPointsOfContender(contender);

    assert pointsAfter >= pointsBefore;
}

// 8.
rule votedCannotBecomeNotVoted(method f, address a) {
    env e;
    calldataarg args;
    bool isVotedBefore = getVoterVoted(a);
    bool isRegistered = getVoterReg(a);
    require isVotedBefore && isRegistered;

    f(e, args);
    bool isVotedAfter = getVoterVoted(a);
    assert isVotedAfter;
}

// 10.
invariant winnerPointsEqualToContenderPoints()
    getContenderIsReg(getWinnerWinner()) => getPointsOfContender(getWinnerWinner()) == getWinnerPoints()

    {
        preserved with(env e) {
            require getContenderIsReg(getWinnerWinner());
        }
    }


// 9.
// invariant winnerHasMorePoints(address a)
//     forall address user. (getContenderIsReg(user) && getContenderIsReg(getWinnerWinner()) && user != getWinnerWinner()) => getWinnerPoints() >= getPointsOfContender(user)
//     // (getWinnerWinner() != a) => (getWinnerPoints() >= getPointsOfContender(a))
//     {
//         preserved with(env e) {
//             require getContenderIsReg(getWinnerWinner()) && getContenderIsReg(a);
//         }

//         preserved registerContender(uint8 age) with (env e2) {
//             require nonContender(e2.msg.sender);
//         }

//         preserved vote(address first, address second, address third) with (env e2) {
//             require getContenderIsReg(first) && getContenderIsReg(second) && getContenderIsReg(third);
//         }
//     }

