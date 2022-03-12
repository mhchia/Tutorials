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
    getOwner() returns (address) envfree

    init_pool()
    add_liquidity() returns (uint256)
    remove_liquidity(uint256)
    swap(address)
    sync()
}


// ## Rules
// ### Valid State
definition isPoolUninitialized() returns bool = (
    getToken0Amount() == 0 &&
    getToken1Amount() == 0 &&
    getK() == 0 &&
    balanceOf(getOwner()) == 0 &&
    totalSupply() == 0
);

definition isPoolInitialized() returns bool = (
    getToken0Amount() > 0 &&
    getToken1Amount() > 0 &&
    getK() > 0 &&
    totalSupply() > 0
);


// ### State Transitions
rule poolInit(method f) {
    env e;
    calldataarg args;
    require isPoolUninitialized();

    // Not interested in `sync`.
    require f.selector != sync().selector;

    f(e, args);

    assert isPoolInitialized() => (
        f.selector == init_pool().selector &&
        e.msg.sender == getOwner()
    );

}

// ### Variable Transitions

rule lpTokenIncreased(method f) {
    uint256 lpBefore = totalSupply();

    env e;
    calldataarg args;
    f(e, args);

    uint256 lpAfter = totalSupply();
    if (f.selector == init_pool().selector) {
        assert lpAfter == 100000;
    } else {
        assert (lpAfter > lpBefore) => (
            f.selector == transfer(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == add_liquidity().selector ||
            f.selector == swap(address).selector
        );
    }
}


// ### High-Level Properties

invariant totalSupply_GE_single_user_balance()
    forall address user. totalSupply() >= balanceOf(user)

// ### Unit-tests

rule add_liquidity(uint256 amount) {
    uint256 totalBefore = totalSupply();
    env e;
    uint256 userBalanceBefore = balanceOf(e.msg.sender);

    require userBalanceBefore >= amount;

    remove_liquidity(e, amount);

    assert totalSupply() == totalBefore - amount;
    assert balanceOf(e.msg.sender) == userBalanceBefore - amount;
}

rule remove_liquidity(uint256 amount) {
    uint256 totalBefore = totalSupply();
    env e;
    uint256 userBalanceBefore = balanceOf(e.msg.sender);
    require userBalanceBefore >= amount;


    remove_liquidity(e, amount);

    assert totalSupply() == totalBefore - amount;
    assert balanceOf(e.msg.sender) == userBalanceBefore - amount;
}



