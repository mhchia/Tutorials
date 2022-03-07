methods {
    getTokenAtIndex(uint256) returns (address) envfree
    getIdOfToken(address) returns (uint256) envfree
    getReserveCount() returns (uint256) envfree
    addReserve(address, address, address, uint256) envfree
    removeReserve(address) envfree
}


invariant BothListsAreCorrelated(uint256 i, address t)
    (
        ((i != 0 && t != 0) => ((getIdOfToken(t) == i) <=> getTokenAtIndex(i) == t)) &&
        ((i == 0) => (getTokenAtIndex(i) == t => getIdOfToken(t) == i))
    )
    {
        preserved addReserve(address token, address stableToken, address varToken, uint256 fee) {
            require token == t;
        }
        preserved removeReserve(address token) {
            require token == t;
        }
    }


// @note this invariant is invalid because `removeReserve` makes
//  `reserveCountAfter <= getIdOfToken(t)` if `getIdOfToken(t) >= reserveCountBefore - 1`.
// invariant NoTokenIndexGTEReserveCounter(address t)
//     // In the initial state, id is equal to reserve count.
//     ((getReserveCount() == 0) => (getIdOfToken(t) == getReserveCount())) &&
//     // If not initial state, id shall be always less than reserve count.
//     ((getReserveCount() != 0) => (getIdOfToken(t) < getReserveCount()))


function hasReserve(address t) returns bool {
    if (t == 0) {
        return false;
    }
    uint256 index = getIdOfToken(t);
    return getTokenAtIndex(index) == t;
}

invariant AssetsToIdIsInjective(address t0, address t1)
    // @note only consider the cases that both t0 and t1 already have reserves.
    (hasReserve(t0) && hasReserve(t1) && t0 != t1) => getIdOfToken(t0) != getIdOfToken(t1)


rule IndependencyOfTokensInList(address t0, address t1) {
    require (t0 != t1) && hasReserve(t0) && hasReserve(t1);

    uint256 t1IdBefore = getIdOfToken(t1);

    removeReserve(t0);

    uint256 t1IdAfter = getIdOfToken(t1);

    assert hasReserve(t1) && (t1IdBefore == t1IdAfter);
}

rule NonViewFunctionChangesReservesCountBy1(method f) {
    require (
        f.selector == addReserve(address, address, address, uint256).selector ||
        f.selector == removeReserve(address).selector
    );

    uint256 reserveCountBefore = getReserveCount();

    env e;
    calldataarg args;
    f(e, args);

    uint256 reserveCountAfter = getReserveCount();

    assert (
        reserveCountBefore == reserveCountAfter + 1 ||
        reserveCountAfter == reserveCountBefore + 1
    );

}

