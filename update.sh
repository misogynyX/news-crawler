#!/usr/bin/env bash
aws s3 ls ${AWS_S3_BUCKET}/news/ \
  | awk '{print $4}' \
  | sort \
  | python cli.py fetch_missings
gzip -f data/*.csv
aws s3 sync --no-progress data s3://${AWS_S3_BUCKET}/news

