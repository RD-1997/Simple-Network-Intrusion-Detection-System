#!/bin/bash

#defining some color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

#stopping the crawler
kill $(ps aux | grep '[p]ython' | awk '{print $2}')

echo ""
echo -e "${RED}Sniffer has been terminated.${NC}"
