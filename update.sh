#!/usr/bin/env bash
LATEST=`aws s3 ls ${AWS_S3_BUCKET}/news/ | awk '{print $4}' | sort | tail -n 1`
python cli.py download_since --latest=${LATEST}
aws s3 sync --no-progress data s3://${AWS_S3_BUCKET}/news

