#!/bin/bash

echo "=========================="
echo "Starting App zoltar for {APP_PRETTY_NAME}"


systemctl start zoltar
systemctl start rosnodeChecker
