#!/bin/bash

# Start TorchServe
torchserve --start --model-store model_artifacts --ts-config config/config.properties

# Keep the container running
tail -f /dev/null
