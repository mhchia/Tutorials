certoraRun ERC20Fixed.sol:ERC20 --verify ERC20:ERC20.spec \
--solc solc8.0 \
--send_only \
--optimistic_loop \
--msg "$1"
