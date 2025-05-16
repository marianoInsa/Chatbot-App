#!/bin/sh

ollama serve &

sleep 5

ollama pull nomic-embed-text

sleep 5

ollama pull llama2

tail -f /dev/null
