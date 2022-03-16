methods {
    get(uint256) returns (uint256) envfree
    contains(uint256) returns (bool) envfree

    insert(uint256, uint256)
    remove(uint256)
}

rule insertRevertConditions(uint key, uint value) {
    env e;
    insert@withrevert(e, key, value);
    bool succeeded = !lastReverted;

    assert (e.msg.value == 0
        && value != 0
        && !contains(key))
        => succeeded;
}

rule inverses(uint key, uint value) {
    env e;
    insert(e, key, value);
    env e2;
    require e2.msg.value == 0;
    remove@withrevert(e2, key);
    bool removeSucceeded = !lastReverted;
    assert removeSucceeded, "remove after insert must succeed";
    assert get(key) != value, "value of removed key must not be the inserted value";
}
