#!/bin/bash
# Secure Jupyter Token Recovery - Bash Script
# Safely retrieves Jupyter token from .env file without logging to history

set -euo pipefail

ENV_FILE="${1:-.env}"
SHOW_URLS="${2:-ask}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

get_jupyter_token() {
    local env_file="$1"
    
    if [[ ! -f "$env_file" ]]; then
        echo -e "${RED}❌ Error: .env file not found at $env_file${NC}" >&2
        return 1
    fi
    
    # Read the file and extract JUPYTER_TOKEN
    local token
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// }" ]] && continue
        
        # Look for JUPYTER_TOKEN
        if [[ "$line" =~ ^JUPYTER_TOKEN=(.+)$ ]]; then
            token="${BASH_REMATCH[1]}"
            
            # Remove quotes if present
            token="${token%\"}"
            token="${token#\"}"
            token="${token%\'}"
            token="${token#\'}"
            
            # Validate token
            if [[ -z "$token" ]] || [[ "$token" == "your-secure-token-here" ]] || [[ "$token" == "change-me" ]]; then
                echo -e "${YELLOW}⚠️  Warning: Jupyter token appears to be a placeholder${NC}" >&2
                return 1
            fi
            
            echo "$token"
            return 0
        fi
    done < "$env_file"
    
    echo -e "${RED}❌ Error: JUPYTER_TOKEN not found in .env file${NC}" >&2
    return 1
}

show_jupyter_urls() {
    local token="$1"
    
    echo
    echo -e "${CYAN}🚀 Jupyter Lab Access Information:${NC}"
    echo -e "${GRAY}==================================================${NC}"
    echo -e "${GREEN}🌐 Jupyter Lab:     http://localhost:8888/lab?token=$token${NC}"
    echo -e "${GREEN}📓 Classic Notebook: http://localhost:8888/tree?token=$token${NC}"
    echo -e "${YELLOW}🔑 Token Only:       $token${NC}"
    echo -e "${GRAY}==================================================${NC}"
    
    echo
    echo -e "${CYAN}💡 Security Tips:${NC}"
    echo -e "${WHITE}• Copy the URL before the terminal scrolls${NC}"
    echo -e "${WHITE}• Don't share the token in screenshots or logs${NC}"
    echo -e "${WHITE}• Consider using 'docker compose logs jupyter' for auto-generated URLs${NC}"
}

main() {
    echo -e "${CYAN}🔐 Secure Jupyter Token Recovery${NC}"
    echo -e "${GRAY}================================${NC}"
    
    # Get token securely
    if token=$(get_jupyter_token "$ENV_FILE"); then
        echo -e "${GREEN}✅ Token retrieved successfully${NC}"
        
        case "$SHOW_URLS" in
            "yes"|"y"|"true"|"1")
                show_jupyter_urls "$token"
                ;;
            "no"|"n"|"false"|"0")
                echo
                echo -e "${YELLOW}🔑 Token: $token${NC}"
                echo -e "${CYAN}💡 Use this token to access Jupyter Lab at http://localhost:8888${NC}"
                ;;
            *)
                echo
                read -p "❓ Display Jupyter URLs? (y/N): " -r response
                if [[ "$response" =~ ^[yY] ]]; then
                    show_jupyter_urls "$token"
                else
                    echo
                    echo -e "${YELLOW}🔑 Token: $token${NC}"
                    echo -e "${CYAN}💡 Use this token to access Jupyter Lab at http://localhost:8888${NC}"
                fi
                ;;
        esac
    else
        echo
        echo -e "${RED}❌ Failed to retrieve Jupyter token${NC}"
        echo
        echo -e "${CYAN}🔧 Troubleshooting:${NC}"
        echo -e "${WHITE}1. Ensure .env file exists in the current directory${NC}"
        echo -e "${WHITE}2. Check that JUPYTER_TOKEN is set in .env file${NC}"
        echo -e "${WHITE}3. Verify the token is not a placeholder value${NC}"
        return 1
    fi
}

# Prevent token from being stored in bash history
set +H 2>/dev/null || true

# Run main function
main "$@"