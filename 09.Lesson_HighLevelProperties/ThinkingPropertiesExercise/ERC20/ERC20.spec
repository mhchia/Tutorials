methods {
	name() returns (string memory) envfree
	symbol() returns (string memory) envfree
	decimals() returns (uint8) envfree
	totalSupply() returns (uint256) envfree
	allowance(address, address) returns (uint256) envfree
	balanceOf(address) returns (uint256) envfree

    transfer(address, uint256) returns (bool)
    approve(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)
    increaseAllowance(address, uint256) returns (bool)
    decreaseAllowance(address, uint256) returns (bool)
}


// 1. allowance increased -> approve, increaseAllowance
rule allowanceIncreased(method f, address a, address b) {
    env e;
    calldataarg args;
    uint256 allowanceBefore = allowance(a, b);

    f(e, args);

    uint256 allowanceAfter = allowance(a, b);

    assert allowanceAfter > allowanceBefore => (
        f.selector == approve(address, uint256).selector ||
        f.selector == increaseAllowance(address, uint256).selector
    );
}


// 2. allowance decreased -> approve, decreaseAllowance, transferFrom
rule allowanceDecreased(method f, address a, address b) {
    env e;
    calldataarg args;
    uint256 allowanceBefore = allowance(a, b);

    f(e, args);

    uint256 allowanceAfter = allowance(a, b);

    assert allowanceAfter < allowanceBefore => (
        f.selector == approve(address, uint256).selector ||
        f.selector == decreaseAllowance(address, uint256).selector ||
        f.selector == transferFrom(address, address, uint256).selector
    );
}


// 3. totalSupply >= user balance
invariant totalSupply_GE_single_user_balance()
    forall address user. totalSupply() >= balanceOf(user)


// 4. transfer, transferFrom: balanceToBefore + balanceFromBefore == balanceToAfter + balanceFromAfter
rule transferAmountSumTheSame(address b, uint256 amount) {
    env e;
    uint256 msgSenderBalanceBefore = balanceOf(e.msg.sender);
    uint256 bBalanceBefore = balanceOf(b);

    transfer(e, b, amount);

    uint256 msgSenderBalanceAfter = balanceOf(e.msg.sender);
    uint256 bBalanceAfter = balanceOf(b);

    assert msgSenderBalanceBefore + bBalanceBefore == msgSenderBalanceAfter + bBalanceAfter;
}

rule transferFromAmountSumTheSame(address sender, address recipient, uint256 amount) {
    env e;
    uint256 senderBalanceBefore = balanceOf(sender);
    uint256 recipientBalanceBefore = balanceOf(recipient);

    transferFrom(e, sender, recipient, amount);

    uint256 senderBalanceAfter = balanceOf(sender);
    uint256 recipientBalanceAfter = balanceOf(recipient);

    assert senderBalanceBefore + recipientBalanceBefore == senderBalanceAfter + recipientBalanceAfter;
}
