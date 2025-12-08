#!/bin/bash

# VRISA Backend Complete Testing Script
# This script tests all API endpoints systematically

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:8000"
API_URL="$BASE_URL/api"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Function to print test results
print_test() {
    local test_name=$1
    local status=$2
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✓${NC} Test #$TESTS_TOTAL: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} Test #$TESTS_TOTAL: $test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Function to make HTTP request and check status
test_request() {
    local method=$1
    local url=$2
    local data=$3
    local expected_status=$4
    local token=$5
    
    if [ -n "$token" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            -d "$data" 2>/dev/null)
    else
        RESPONSE=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null)
    fi
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" = "$expected_status" ]; then
        echo "$BODY"
        return 0
    else
        echo "Expected: $expected_status, Got: $HTTP_CODE" >&2
        echo "Response: $BODY" >&2
        return 1
    fi
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   VRISA BACKEND TESTING SUITE${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ==================== PRELIMINARY CHECKS ====================
echo -e "${YELLOW}>>> Running preliminary checks...${NC}"

# Test 1: Health Check
echo -n "Checking health endpoint... "
if HEALTH=$(test_request GET "$BASE_URL/health/" "" "200"); then
    print_test "Health Check" "PASS"
    echo "  Database: $(echo $HEALTH | jq -r '.database')"
    echo "  Redis: $(echo $HEALTH | jq -r '.redis')"
else
    print_test "Health Check" "FAIL"
    echo -e "${RED}❌ Backend is not healthy. Aborting tests.${NC}"
    exit 1
fi

# Test 2: API Root
echo -n "Checking API root... "
if test_request GET "$BASE_URL/" "" "200" > /dev/null; then
    print_test "API Root Accessible" "PASS"
else
    print_test "API Root Accessible" "FAIL"
fi

echo ""

# ==================== AUTHENTICATION TESTS ====================
echo -e "${YELLOW}>>> Testing Authentication Endpoints...${NC}"

# Test 3: Register User
echo -n "Registering new user... "
REGISTER_DATA='{
    "name": "Test User",
    "email": "test@vrisa.com",
    "password": "testpass123",
    "role": "citizen"
}'

if REGISTER_RESPONSE=$(test_request POST "$API_URL/auth/register/" "$REGISTER_DATA" "201"); then
    print_test "User Registration" "PASS"
    USER_TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.tokens.access')
    USER_ID=$(echo $REGISTER_RESPONSE | jq -r '.user.id')
    echo "  User ID: $USER_ID"
else
    print_test "User Registration" "FAIL"
    USER_TOKEN=""
    USER_ID=""
fi

# Test 4: Login
echo -n "Testing login... "
LOGIN_DATA='{
    "email": "test@vrisa.com",
    "password": "testpass123"
}'

if LOGIN_RESPONSE=$(test_request POST "$API_URL/auth/login/" "$LOGIN_DATA" "200"); then
    print_test "User Login" "PASS"
    USER_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access')
else
    print_test "User Login" "FAIL"
fi

# Test 5: Verify Token
echo -n "Verifying JWT token... "
if test_request GET "$API_URL/auth/verify/" "" "200" "$USER_TOKEN" > /dev/null; then
    print_test "Token Verification" "PASS"
else
    print_test "Token Verification" "FAIL"
fi

# Test 6: Get Current User
echo -n "Getting current user profile... "
if test_request GET "$API_URL/users/me/" "" "200" "$USER_TOKEN" > /dev/null; then
    print_test "Get Current User" "PASS"
else
    print_test "Get Current User" "FAIL"
fi

echo ""

# ==================== ADMIN TESTS ====================
echo -e "${YELLOW}>>> Testing Admin Endpoints...${NC}"

# Test 7: Create Admin User
echo -n "Creating admin user... "
ADMIN_DATA='{
    "access_level": 5,
    "user": {
        "name": "Admin User",
        "email": "admin@vrisa.com",
        "password": "admin123",
        "role": "admin"
    }
}'

if ADMIN_RESPONSE=$(test_request POST "$API_URL/admins/" "$ADMIN_DATA" "201" "$USER_TOKEN"); then
    print_test "Create Admin" "PASS"
    ADMIN_ID=$(echo $ADMIN_RESPONSE | jq -r '.id')
    echo "  Admin ID: $ADMIN_ID"
else
    print_test "Create Admin" "FAIL"
    ADMIN_ID=""
fi

# Test 8: Admin Login
echo -n "Logging in as admin... "
ADMIN_LOGIN='{
    "email": "admin@vrisa.com",
    "password": "admin123"
}'

if ADMIN_LOGIN_RESPONSE=$(test_request POST "$API_URL/auth/login/" "$ADMIN_LOGIN" "200"); then
    print_test "Admin Login" "PASS"
    ADMIN_TOKEN=$(echo $ADMIN_LOGIN_RESPONSE | jq -r '.access')
else
    print_test "Admin Login" "FAIL"
    ADMIN_TOKEN=""
fi

# Test 9: List Admins
echo -n "Listing all admins... "
if test_request GET "$API_URL/admins/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Admins" "PASS"
else
    print_test "List Admins" "FAIL"
fi

echo ""

# ==================== AUTH USER TESTS ====================
echo -e "${YELLOW}>>> Testing Auth User Endpoints...${NC}"

# Test 10: Create Auth User
echo -n "Creating authorized user... "
AUTH_USER_DATA='{
    "read_access": true,
    "user": {
        "name": "Researcher",
        "email": "researcher@vrisa.com",
        "password": "research123",
        "role": "researcher"
    }
}'

if AUTH_USER_RESPONSE=$(test_request POST "$API_URL/auth-users/" "$AUTH_USER_DATA" "201" "$ADMIN_TOKEN"); then
    print_test "Create Auth User" "PASS"
    AUTH_USER_ID=$(echo $AUTH_USER_RESPONSE | jq -r '.id')
    echo "  Auth User ID: $AUTH_USER_ID"
else
    print_test "Create Auth User" "FAIL"
    AUTH_USER_ID=""
fi

# Test 11: List Auth Users
echo -n "Listing auth users... "
if test_request GET "$API_URL/auth-users/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Auth Users" "PASS"
else
    print_test "List Auth Users" "FAIL"
fi

echo ""

# ==================== INSTITUTION TESTS ====================
echo -e "${YELLOW}>>> Testing Institution Endpoints...${NC}"

# Test 12: Create Institution
echo -n "Creating institution... "
INSTITUTION_DATA='{
    "name": "Environmental Agency Cali",
    "address": "Calle 5 #10-20, Cali",
    "verified": true,
    "admin": '$ADMIN_ID'
}'

if INSTITUTION_RESPONSE=$(test_request POST "$API_URL/institutions/" "$INSTITUTION_DATA" "201" "$ADMIN_TOKEN"); then
    print_test "Create Institution" "PASS"
    INSTITUTION_ID=$(echo $INSTITUTION_RESPONSE | jq -r '.id')
    echo "  Institution ID: $INSTITUTION_ID"
else
    print_test "Create Institution" "FAIL"
    INSTITUTION_ID=""
fi

# Test 13: List Institutions
echo -n "Listing institutions... "
if test_request GET "$API_URL/institutions/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Institutions" "PASS"
else
    print_test "List Institutions" "FAIL"
fi

# Test 14: Get Institution Detail
echo -n "Getting institution detail... "
if test_request GET "$API_URL/institutions/$INSTITUTION_ID/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Get Institution Detail" "PASS"
else
    print_test "Get Institution Detail" "FAIL"
fi

# Test 15: Filter Verified Institutions
echo -n "Filtering verified institutions... "
if test_request GET "$API_URL/institutions/?verified=true" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Filter Institutions" "PASS"
else
    print_test "Filter Institutions" "FAIL"
fi

echo ""

# ==================== STATION TESTS ====================
echo -e "${YELLOW}>>> Testing Station Endpoints...${NC}"

# Test 16: Create Station
echo -n "Creating station... "
STATION_DATA='{
    "name": "Station Centro",
    "description": "Air quality monitoring station in city center",
    "address": "Carrera 10 #5-50, Cali",
    "institution": '$INSTITUTION_ID',
    "admin": '$ADMIN_ID',
    "location": [-76.5319, 3.4516],
    "status": "active",
    "installed_at": "2024-01-15"
}'

if STATION_RESPONSE=$(test_request POST "$API_URL/stations/" "$STATION_DATA" "201" "$ADMIN_TOKEN"); then
    print_test "Create Station" "PASS"
    STATION_ID=$(echo $STATION_RESPONSE | jq -r '.id')
    echo "  Station ID: $STATION_ID"
else
    print_test "Create Station" "FAIL"
    STATION_ID=""
fi

# Test 17: List Stations
echo -n "Listing stations... "
if test_request GET "$API_URL/stations/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Stations" "PASS"
else
    print_test "List Stations" "FAIL"
fi

# Test 18: Get Station Detail
echo -n "Getting station detail... "
if test_request GET "$API_URL/stations/$STATION_ID/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Get Station Detail" "PASS"
else
    print_test "Get Station Detail" "FAIL"
fi

# Test 19: Filter Stations by Status
echo -n "Filtering active stations... "
if test_request GET "$API_URL/stations/?status=active" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Filter Stations by Status" "PASS"
else
    print_test "Filter Stations by Status" "FAIL"
fi

# Test 20: Search Stations
echo -n "Searching stations by name... "
if test_request GET "$API_URL/stations/?search=centro" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Search Stations" "PASS"
else
    print_test "Search Stations" "FAIL"
fi

# Test 21: Nearby Stations (Spatial Query)
echo -n "Finding nearby stations... "
if test_request GET "$API_URL/stations/nearby/?lat=3.4516&lon=-76.5319&radius=5000" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Nearby Stations (PostGIS)" "PASS"
else
    print_test "Nearby Stations (PostGIS)" "FAIL"
fi

echo ""

# ==================== DEVICE TESTS ====================
echo -e "${YELLOW}>>> Testing Device Endpoints...${NC}"

# Test 22: Create Device
echo -n "Creating device... "
DEVICE_DATA='{
    "serial_number": "SENSOR-001",
    "description": "PM2.5 and PM10 sensor",
    "type": "SENSOR",
    "station": '$STATION_ID'
}'

if DEVICE_RESPONSE=$(test_request POST "$API_URL/devices/" "$DEVICE_DATA" "201" "$ADMIN_TOKEN"); then
    print_test "Create Device" "PASS"
    DEVICE_ID=$(echo $DEVICE_RESPONSE | jq -r '.id')
    echo "  Device ID: $DEVICE_ID"
else
    print_test "Create Device" "FAIL"
    DEVICE_ID=""
fi

# Test 23: List Devices
echo -n "Listing devices... "
if test_request GET "$API_URL/devices/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Devices" "PASS"
else
    print_test "List Devices" "FAIL"
fi

# Test 24: Filter Devices by Station
echo -n "Filtering devices by station... "
if test_request GET "$API_URL/devices/?station=$STATION_ID" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Filter Devices by Station" "PASS"
else
    print_test "Filter Devices by Station" "FAIL"
fi

echo ""

# ==================== ALERT TESTS ====================
echo -e "${YELLOW}>>> Testing Alert Endpoints...${NC}"

# Test 25: Create Alert
echo -n "Creating alert... "
ALERT_DATA='{
    "station": '$STATION_ID',
    "attended": false
}'

if ALERT_RESPONSE=$(test_request POST "$API_URL/alerts/" "$ALERT_DATA" "201" "$ADMIN_TOKEN"); then
    print_test "Create Alert" "PASS"
    ALERT_ID=$(echo $ALERT_RESPONSE | jq -r '.id')
    echo "  Alert ID: $ALERT_ID"
else
    print_test "Create Alert" "FAIL"
    ALERT_ID=""
fi

# Test 26: Add Pollutants to Alert ⭐
echo -n "Adding pollutants to alert... "
POLLUTANTS_DATA='{
    "pollutants": [
        {
            "pollutant": "PM25",
            "level": 55.3
        },
        {
            "pollutant": "NO2",
            "level": 42.1
        },
        {
            "pollutant": "O3",
            "level": 78.5
        }
    ]
}'

if test_request POST "$API_URL/alerts/$ALERT_ID/pollutants/" "$POLLUTANTS_DATA" "201" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Add Pollutants to Alert ⭐" "PASS"
else
    print_test "Add Pollutants to Alert ⭐" "FAIL"
fi

# Test 27: Get Alert with Pollutants
echo -n "Getting alert with pollutants... "
if ALERT_DETAIL=$(test_request GET "$API_URL/alerts/$ALERT_ID/" "" "200" "$ADMIN_TOKEN"); then
    print_test "Get Alert Detail" "PASS"
    POLLUTANT_COUNT=$(echo $ALERT_DETAIL | jq '.pollutants | length')
    echo "  Pollutants found: $POLLUTANT_COUNT"
else
    print_test "Get Alert Detail" "FAIL"
fi

# Test 28: Get Station Alerts ⭐
echo -n "Getting all alerts for station... "
if STATION_ALERTS=$(test_request GET "$API_URL/stations/$STATION_ID/alerts/" "" "200" "$ADMIN_TOKEN"); then
    print_test "Get Station Alerts ⭐" "PASS"
    ALERT_COUNT=$(echo $STATION_ALERTS | jq '.results | length')
    echo "  Alerts found: $ALERT_COUNT"
else
    print_test "Get Station Alerts ⭐" "FAIL"
fi

# Test 29: Filter Unattended Alerts
echo -n "Filtering unattended alerts... "
if test_request GET "$API_URL/alerts/?attended=false" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Filter Unattended Alerts" "PASS"
else
    print_test "Filter Unattended Alerts" "FAIL"
fi

# Test 30: Mark Alert as Attended
echo -n "Marking alert as attended... "
if test_request POST "$API_URL/alerts/$ALERT_ID/mark-attended/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Mark Alert Attended" "PASS"
else
    print_test "Mark Alert Attended" "FAIL"
fi

echo ""

# ==================== STATION ACCESS TESTS ====================
echo -e "${YELLOW}>>> Testing Station Access Control...${NC}"

# Test 31: Grant Station Access to Auth User
echo -n "Granting station access to auth user... "
GRANT_DATA='{
    "auth_user_id": '$AUTH_USER_ID'
}'

if test_request POST "$API_URL/stations/$STATION_ID/grant-access/" "$GRANT_DATA" "201" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Grant Station Access ⭐" "PASS"
else
    print_test "Grant Station Access ⭐" "FAIL"
fi

# Test 32: List Station Consults
echo -n "Listing station access permissions... "
if test_request GET "$API_URL/station-consults/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Station Consults" "PASS"
else
    print_test "List Station Consults" "FAIL"
fi

# Test 33: Notify Users about Alert
echo -n "Recording alert notifications... "
NOTIFY_DATA='{
    "auth_user_ids": ['$AUTH_USER_ID']
}'

if test_request POST "$API_URL/alerts/$ALERT_ID/notify/" "$NOTIFY_DATA" "201" "$ADMIN_TOKEN" > /dev/null; then
    print_test "Notify Alert Users ⭐" "PASS"
else
    print_test "Notify Alert Users ⭐" "FAIL"
fi

# Test 34: List Alert Receives
echo -n "Listing alert notifications... "
if test_request GET "$API_URL/alert-receives/" "" "200" "$ADMIN_TOKEN" > /dev/null; then
    print_test "List Alert Receives" "PASS"
else
    print_test "List Alert Receives" "FAIL"
fi

echo ""

# ==================== PERMISSION TESTS ====================
echo -e "${YELLOW}>>> Testing Permission Controls...${NC}"

# Test 35: Non-admin tries to create institution (should fail)
echo -n "Testing non-admin institution creation (should fail)... "
if test_request POST "$API_URL/institutions/" "$INSTITUTION_DATA" "403" "$USER_TOKEN" > /dev/null 2>&1; then
    print_test "Permission: Non-admin Blocked" "PASS"
else
    print_test "Permission: Non-admin Blocked" "FAIL"
fi

# Test 36: Unauthenticated access (should fail)
echo -n "Testing unauthenticated access (should fail)... "
if test_request GET "$API_URL/stations/" "" "401" > /dev/null 2>&1; then
    print_test "Permission: Unauthenticated Blocked" "PASS"
else
    print_test "Permission: Unauthenticated Blocked" "FAIL"
fi

echo ""

# ==================== PAGINATION TESTS ====================
echo -e "${YELLOW}>>> Testing Pagination...${NC}"

# Test 37: Pagination Parameters
echo -n "Testing pagination with page_size... "
if PAGINATED=$(test_request GET "$API_URL/stations/?page=1&page_size=5" "" "200" "$ADMIN_TOKEN"); then
    print_test "Pagination Parameters" "PASS"
    TOTAL=$(echo $PAGINATED | jq -r '.count')
    CURRENT_PAGE=$(echo $PAGINATED | jq -r '.current_page')
    echo "  Total items: $TOTAL, Current page: $CURRENT_PAGE"
else
    print_test "Pagination Parameters" "FAIL"
fi

echo ""

# ==================== FINAL SUMMARY ====================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}         TEST RESULTS SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Total Tests:  ${BLUE}$TESTS_TOTAL${NC}"
echo -e "Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed:       ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}✓ Backend is ready for frontend development!${NC}"
    exit 0
else
    PASS_RATE=$((TESTS_PASSED * 100 / TESTS_TOTAL))
    echo -e "${YELLOW}⚠ Some tests failed (Pass rate: $PASS_RATE%)${NC}"
    
    if [ $PASS_RATE -ge 80 ]; then
        echo -e "${YELLOW}Backend is mostly functional. You can proceed with caution.${NC}"
        exit 0
    else
        echo -e "${RED}❌ Too many failures. Fix issues before proceeding.${NC}"
        exit 1
    fi
fi
