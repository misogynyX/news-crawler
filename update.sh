#!/usr/bin/env bash
poetry install
aws s3 sync s3://${AWS_S3_BUCKET}/news data
python cli.py download
aws s3 sync data s3://${AWS_S3_BUCKET}/news

