methods{
    slow_copy(uint) returns uint envfree
    const_loop() returns uint envfree
}

// slow_copy() always returns the input value
rule slow_copy_correct(uint n) {
    // @note Pass with `--optimistic_loop` since default `loop_iter` is 1 and `slow_copy(n)` returns 1.
    assert slow_copy(n) == n, "slow_copy(n) always returns n";
}

// This rule should fail as slow_copy(n) should always return n
rule slow_copy_wrong(uint n) {
    // @note Fails with `--optimistic_loop` since default `loop_iter` is 1, then `slow_copy(n)` returns 1 instead of 2*n.
    assert slow_copy(n) == 2*n, "slow_copy(n) returned a value other than 2*n";
}

// const_loop always returns 5
rule const_loop_correct(){
    // @note
    //  In optimistic,
    //      - Always pass no matter `loop_iter`, because loop always returns `n`, the number of loop has done.
    //          - `loop_iter < 5`   -> because of the optimistic mode, since constant number is 5,
    //              `require(!(i < 5))` demanded by optimistic rule and it is a vacuous rule (every i reverts),
    //              which makes us never reach the assert and thus always true.
    //          - `loop_iter >= 5`  -> since constant loop, we always do 5 loops and return.
    //  In pessimistic
    //      - if loop_iter < constant number, fails.
    //      - else, returns 5.
    assert const_loop() == 5, "The function returned a value other than 5";
    // assert false, "not vacuous";
}

// This rule should fail as const_loop should always return 5
rule const_loop_wrong(){
    // @note
    //  In optimistic,
    //      - if `loop_iter < 5`    -> vacuous rule and thus always passes.
    //      - if `loop_iter >= 5`   -> num of loops done is returned and thus 5, so always fails.
    //  In pessimistic
    //      - if loop_iter < constant number, fails.
    //      - else, returns 5.
    assert const_loop() == 3, "The function returned a value other than 3";
    // assert false, "not vacuous";
}