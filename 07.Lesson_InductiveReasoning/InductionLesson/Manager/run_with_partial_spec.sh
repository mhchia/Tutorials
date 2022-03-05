certoraRun "$1:Manager" --verify Manager:ManagerPartialSolution.spec \
--solc solc8.6 \
--msg "Partial: $1 $2" \
--send_only
