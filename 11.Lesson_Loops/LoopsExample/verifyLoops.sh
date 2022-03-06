certoraRun Loops.sol:Loops --verify Loops:LoopsUnrolling.spec \
--solc solc8.11 \
--send_only \
--optimistic_loop \
--loop_iter 10 \
--msg "$1"