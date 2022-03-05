
methods {
	ballAt() returns uint256 envfree
	pass()
}

definition ballNotAt3or4() returns bool = ballAt() != 3 && ballAt() != 4;

invariant neverReachPlayer4()
	ballNotAt3or4()


rule translation_of_neverReachPlayer4(method f){
	env e;
	calldataarg args;
	// https://certora.atlassian.net/wiki/spaces/CPD/pages/7340088/The+Bank
    require ballNotAt3or4();
    f(e, args);
    assert ballAt() != 4;
}
