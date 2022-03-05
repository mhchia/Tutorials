certoraRun BankFixed.sol:Bank --verify Bank:invariant.spec \
--solc solc7.6 \
--send_only \
--msg "$1"