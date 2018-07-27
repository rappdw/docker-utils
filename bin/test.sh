#!/usr/bin/env bash

pytest --cov=dockerutils --cov-report=term-missing --cov-fail-under=75 --durations=10 tests