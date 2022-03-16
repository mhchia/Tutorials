rule MethodsVacuityCheck(method f) {
	env e; calldataarg args;
	f(e, args);
	// If all paths were to revert before reaching our assert false,
	// this assert will have never been checked in the first place and thus the rule passes.
	assert false, "this method should have a non reverting path";
}

invariant vacuousInvariant(uint x, address y)
    x > 2

rule checkVacuousInvariants(uint x, address y) {
	// Only pass if the expression is a tautology: because it's a rule instead of an invariant, inputs are
	// arbitrarily generated and thus assert will fail unless it's an tautology.
	assert x > 2;
}
