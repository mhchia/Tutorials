certoraRun BankWithLoops.sol:Bank --verify Bank:Loops.spec \
--solc solc7.6 \
--send_only \
--loop_iter 2 \
--optimistic_loop \
--msg "$1"