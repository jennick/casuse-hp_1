#!/bin/sh
set -e

# Run cleanup
python -m services.cleanup_customers
