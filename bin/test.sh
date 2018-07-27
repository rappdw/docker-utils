#!/usr/bin/env bash

pytest --cov --cov-report=term-missing --cov-fail-under=75 --durations=10 tests