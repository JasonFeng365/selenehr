@echo off

PUSHD %1
del testcases.zip
cd testcases
zip ../testcases.zip input/*
zip ../testcases.zip output/*
POPD