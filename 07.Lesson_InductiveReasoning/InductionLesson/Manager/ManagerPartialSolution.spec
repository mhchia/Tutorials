methods {
		getCurrentManager(uint256 fundId) returns (address) envfree
		getPendingManager(uint256 fundId) returns (address) envfree
		isActiveManager(address a) returns (bool) envfree
}



rule uniqueManager(uint256 fundId1, uint256 fundId2, method f) {
	require fundId1 != fundId2;
	// The original inputs are so strict that none of them can be called by `createFund` without reverting by
	// `require(funds[fundId].currentManager == address(0));`, and thus no violations (because reverting cases
	// are ignored).
	// Solution: allows one fundId can be an event without initialized.
	require getCurrentManager(fundId1) != 0 => isActiveManager(getCurrentManager(fundId1));
	require getCurrentManager(fundId2) != 0 => isActiveManager(getCurrentManager(fundId2));
	require getCurrentManager(fundId1) != getCurrentManager(fundId2) ;

	env e;
	if (f.selector == claimManagement(uint256).selector)
	{
		uint256 id;
		require id == fundId1 || id == fundId2;
		claimManagement(e, id);
	}
	else {
		calldataarg args;
		f(e,args);
	}
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
	assert getCurrentManager(fundId1) != 0 && isActiveManager(getCurrentManager(fundId1)), "manager of fund1 is not active";
	assert getCurrentManager(fundId2) != 0 && isActiveManager(getCurrentManager(fundId2)), "manager of fund2 is not active";
}





