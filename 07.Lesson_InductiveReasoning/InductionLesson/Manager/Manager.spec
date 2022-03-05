methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}


// an address can manage only one fund
rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	address manager1 = getCurrentManager(fundId1);
	address manager2 = getCurrentManager(fundId2);
	require isActiveManager(manager1) && isActiveManager(manager2) && manager1 != manager2;

	// hint: add additional variables just to look at the current state
	// bool active1 = isActiveManager(getCurrentManager(fundId1));

	env e;
	calldataarg args;
	f(e,args);

	// verify that the managers are still different
	address manager1After = getCurrentManager(fundId1);
	address manager2After = getCurrentManager(fundId2);
	assert manager1After != manager2After, "managers not different";
}


/* A version of uniqueManagerAsRule as an invariant */
invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2)
