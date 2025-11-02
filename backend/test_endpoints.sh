#!/bin/bash
# SIFT API Smoke Tests for Render Deployment
# Usage: ./test_endpoints.sh <BASE_URL>
# Example: ./test_endpoints.sh https://sift-api.onrender.com

BASE_URL="${1:-http://localhost:8000}"

echo "🧪 Testing SIFT API at: $BASE_URL"
echo ""

# Test 1: Health Check
echo "1️⃣ Testing health check endpoint..."
curl -s "$BASE_URL/" | jq '.' || echo "❌ Health check failed"
echo ""

# Test 2: API Docs
echo "2️⃣ Checking API docs..."
curl -s -o /dev/null -w "Status: %{http_code}\n" "$BASE_URL/docs"
echo ""

# Test 3: Text Analysis
echo "3️⃣ Testing text analysis endpoint..."
curl -s -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "The moon landing in 1969 was a hoax."}' | jq '.' || echo "❌ Text analysis failed"
echo ""

# Test 4: URL Analysis (with a known URL)
echo "4️⃣ Testing URL analysis endpoint..."
curl -s -X POST "$BASE_URL/api/v1/analyze/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news"}' | jq '.' || echo "❌ URL analysis failed"
echo ""

# Test 5: CORS Headers
echo "5️⃣ Testing CORS headers..."
curl -s -I -X OPTIONS "$BASE_URL/api/v1/analyze" \
  -H "Origin: https://example.netlify.app" \
  -H "Access-Control-Request-Method: POST" | grep -i "access-control" || echo "⚠️ CORS headers not found"
echo ""

echo "✅ Smoke tests completed!"
echo ""
echo "Note: If tests fail, check:"
echo "  - Environment variables are set correctly"
echo "  - API keys are valid"
echo "  - Service is running and accessible"

