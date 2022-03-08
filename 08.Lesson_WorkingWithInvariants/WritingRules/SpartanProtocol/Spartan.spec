methods {
    // ERC20
    decimals() returns (uint256) envfree
	totalSupply() returns (uint256) envfree
	balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)

    // Spartan
    getContractAddress() returns (address) envfree
    getToken0DepositAddress() returns (address) envfree
    getToken1DepositAddress() returns (address) envfree
    getActualToken0Balance() returns (uint256) envfree
    getActualToken1Balance() returns (uint256) envfree
    getToken0Amount() returns (uint256) envfree
    getToken1Amount() returns (uint256) envfree
    getK() returns (uint256) envfree

    init_pool()
    add_liquidity() returns (uint256)
    remove_liquidity(uint256)
    swap(address)
    sync()
}


// ## Rules
// ### Valid State
// no actual token balance => tokenSupply == 0
invariant noTokenBalanceThenNoLP()
    (getActualToken0Balance() == 0 && getActualToken1Balance() == 0) => (totalSupply() == 100000)


// ### State Transitions
// 2. (userBalanceBefore = 0 and userBalanceAfter > 0) => ((f.selector = deposit(uint256)) or (f.selector == transferFrom(address, address, uint256)) or (f.selector == transfer(address, uint256)))
// LP token increased -> add_liquidity
rule lpTokenIncreased(method f) {
    uint256 lpBefore = totalSupply();

    env e;
    calldataarg args;
    f(e, args);

    uint256 lpAfter = totalSupply();
    assert (lpAfter > lpBefore) => (
        f.selector == transfer(address, uint256).selector ||
        f.selector == transferFrom(address, address, uint256).selector ||
        f.selector == add_liquidity().selector ||
        f.selector == swap(address).selector ||
        f.selector == init_pool().selector
    );
}

// ### Variable Transitions
// 3. After every call f(env, args), totalFeesEarnedPerShareBefore <= totalFeesEarnedPerShareAfter. It's because totalFeesEarnedPerShare should be increased over time.
// token0Amount and token1Amount are increased only after add_liquidity or swap

// ### High-Level Properties
invariant uvk()
    true

// balanceOf >= tokenAmount
// - # LP tokens ==
// token0Amount ==
// 4. ERC20: totalSupply() = balanceOf(user) for all user in users
// 5. assetsOf(user) shall be only non-decreasing if user hasn't transfer/transferFrom/withdraw

// ### Unit-tests
// rule syncCan() {

// }
//



