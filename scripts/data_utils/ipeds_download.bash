#!/bin/bash

cat ../../data_ingest/ipeds/sources/ipeds_2022_download_urls | xargs curl --remote-name-all

