#!/bin/bash

if [ ! -d "result" ]; then
	mkdir result
fi

./domain.py -l >> result/log &
