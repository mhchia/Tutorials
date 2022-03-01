#!/bin/sh

MEETINGS_SPEC_DIR=../../04.Lesson_Declarations/Methods_Definitions_Functions/MeetingScheduler
ls $MEETINGS_SPEC_DIR;
cd $MEETINGS_SPEC_DIR;

certoraRun MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--rule checkPendingToCancelledOrStarted \
--msg "try_parametric_rule_without_specified_method"
