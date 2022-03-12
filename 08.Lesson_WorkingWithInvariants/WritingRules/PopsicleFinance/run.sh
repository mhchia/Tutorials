certoraRun popsicle.sol:PopsicleFinance --verify PopsicleFinance:Popsicle.spec \
--solc solc8.4 \
--send_only \
--optimistic_loop \
--msg "$1"
