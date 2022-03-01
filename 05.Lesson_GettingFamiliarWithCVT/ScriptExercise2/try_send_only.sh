#!/bin/sh

MEETINGS_SPEC_DIR=../../04.Lesson_Declarations/Methods_Definitions_Functions/MeetingScheduler
ls $MEETINGS_SPEC_DIR;
cd $MEETINGS_SPEC_DIR;

certoraRun MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--send_only \
--msg "try_send_only"
