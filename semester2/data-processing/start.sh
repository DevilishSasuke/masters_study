#!/bin/bash
if [ ! -d "grafana_data" ]; then
    mkdir grafana_data
fi

chmod -R 777 grafana_data
docker compose up -d --build