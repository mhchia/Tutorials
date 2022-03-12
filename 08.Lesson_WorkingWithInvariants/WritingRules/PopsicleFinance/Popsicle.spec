methods {
    balanceOf(address) returns (uint256) envfree
    totalSupply() returns (uint256) envfree
    getTotalFeesEarnedPerShare() returns (uint256) envfree
    getOwner() returns (address) envfree
    getFeesCollectedPerShare(address) returns (uint256) envfree
    getRewards(address) returns (uint256) envfree

    assetsOf(address) returns (uint256) envfree

    deposit()
    withdraw(uint256)
    collectFees()
    OwnerDoItsJobAndEarnsFeesToItsClients()

}



// ## Rules
// ### Valid State
// 1. stateNoUser => all balances and accounts should be empty.

// ### State Transitions

// ### Variable Transitions
// 3. After every call f(env, args), totalFeesEarnedPerShareBefore <= totalFeesEarnedPerShareAfter. It's because totalFeesEarnedPerShare should be increased over time.
// @note This fail because `OwnerDoItsJobAndEarnsFeesToItsClients` has no access control while it should have.
rule totalFeesEarnedPerShareIncreased(method f) {
    env e;
    calldataarg args;

    uint256 totalFeesEarnedPerShareBefore = getTotalFeesEarnedPerShare();
    uint256 owner = getOwner();

    f(e, args);
    uint256 totalFeesEarnedPerShareAfter = getTotalFeesEarnedPerShare();

    assert (totalFeesEarnedPerShareBefore < totalFeesEarnedPerShareAfter) => (
        f.selector == OwnerDoItsJobAndEarnsFeesToItsClients().selector &&
        e.msg.sender == owner
    );
}

// ### High-Level Properties

ghost sum_of_all_balances() returns uint256{
    // for the constructor - assuming that on the constructor the value of the ghost is 0
    init_state axiom sum_of_all_balances() == 0;
}

hook Sstore balances[KEY address user] uint256 new_balance
    // the old value ↓ already there
    (uint256 old_balance) STORAGE {
    /* havoc is a reserved keyword that basically changes the state of the ghost (sumAllFunds) to any state.
     * the assuming command the havoc to take into consideration the following clause.
     * the @new and @old additions to the ghost are incarnations of the ghost
     * we basically say here create new incarnation (@new) that is equal to the old incarnation (@old)
     * plus the difference between the new value stored and the old value stored.
     * remember that the new value is the sum of the old + the an addition, so adding @old to the new will be a wrong count
     */
  havoc sum_of_all_balances assuming sum_of_all_balances@new() == sum_of_all_balances@old() + new_balance - old_balance;
}

invariant totalSupplySumBalances()
    totalSupply() == sum_of_all_balances()


// ### Unit Tests

rule depositShouldWork() {
    env e;

    uint256 totalFeesEarnedPerShare = getTotalFeesEarnedPerShare();

    uint256 userFeeCollectedPerShareBefore = getFeesCollectedPerShare(e.msg.sender);
    uint256 userRewardsBefore = getRewards(e.msg.sender);
    uint256 userBalanceBefore = balanceOf(e.msg.sender);

    deposit(e);

    uint256 userFeeCollectedPerShareAfter = getFeesCollectedPerShare(e.msg.sender);
    uint256 userRewardsAfter = getRewards(e.msg.sender);
    uint256 userBalanceAfter = balanceOf(e.msg.sender);
    uint256 newRewards = userBalanceBefore * (totalFeesEarnedPerShare - userFeeCollectedPerShareBefore);

    assert (
        // rewards related
        totalFeesEarnedPerShare == userFeeCollectedPerShareAfter &&
        userRewardsAfter == newRewards + userRewardsBefore &&
        // balance
        userBalanceAfter == userBalanceBefore + e.msg.value
    );
}

// @note this rule shall fail since `userFeeCollectedPerShareAfter` is not updated and
//  rewards should be calculated with balance instead of amount.
rule withdrawShouldWork(uint256 amount) {
    env e;

    uint256 totalFeesEarnedPerShare = getTotalFeesEarnedPerShare();

    uint256 userFeeCollectedPerShareBefore = getFeesCollectedPerShare(e.msg.sender);
    uint256 userRewardsBefore = getRewards(e.msg.sender);
    uint256 userBalanceBefore = balanceOf(e.msg.sender);

    withdraw(e, amount);

    uint256 userFeeCollectedPerShareAfter = getFeesCollectedPerShare(e.msg.sender);
    uint256 userRewardsAfter = getRewards(e.msg.sender);
    uint256 userBalanceAfter = balanceOf(e.msg.sender);
    uint256 newRewards = userBalanceBefore * (totalFeesEarnedPerShare - userFeeCollectedPerShareBefore);

    assert (
        // rewards related
        totalFeesEarnedPerShare == userFeeCollectedPerShareAfter &&
        userRewardsAfter == newRewards + userRewardsBefore &&
        // balance
        userBalanceAfter == userBalanceBefore - amount
    );
}
