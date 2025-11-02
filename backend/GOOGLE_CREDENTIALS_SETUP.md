# How to Set GOOGLE_CREDENTIALS_JSON Environment Variable

This guide explains exactly what value to put in `GOOGLE_CREDENTIALS_JSON` for Render deployment.

## What is GOOGLE_CREDENTIALS_JSON?

This is for **Google Cloud Translation API** credentials. You need to provide your Google Cloud service account credentials as a JSON string.

## Step-by-Step Instructions

### Step 1: Get Your Service Account JSON File

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Select your project (or create one)

2. **Navigate to Service Accounts**
   - Go to: **IAM & Admin** → **Service Accounts**
   - Click **+ CREATE SERVICE ACCOUNT** (if you don't have one)

3. **Create or Select Service Account**
   - Name: `sift-translation-service` (or any name)
   - Click **CREATE AND CONTINUE**
   - Grant role: **Cloud Translation API User**
   - Click **CONTINUE** → **DONE**

4. **Download JSON Key**
   - Click on your service account
   - Go to **Keys** tab
   - Click **ADD KEY** → **Create new key**
   - Select **JSON** format
   - Click **CREATE**
   - A JSON file will download to your computer

### Step 2: Open the JSON File

The downloaded file will look something like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service@your-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

### Step 3: Copy the ENTIRE Contents

1. **Open the JSON file** in a text editor (Notepad, VS Code, etc.)
2. **Select ALL** (Ctrl+A / Cmd+A)
3. **Copy** (Ctrl+C / Cmd+C)

**Important:** Copy EVERYTHING from the file, including:
- Opening `{`
- All fields (type, project_id, private_key, etc.)
- Closing `}`

### Step 4: Paste in Render

1. **Go to Render Dashboard**
   - Your service → **Environment** tab
   - Click **Add Environment Variable**

2. **Set the Variable:**
   - **Key:** `GOOGLE_CREDENTIALS_JSON`
   - **Value:** Paste the ENTIRE JSON content you copied
   - Click **Save Changes**

3. **Render will automatically restart** your service

## Example

Here's what it looks like in Render:

```
Key:   GOOGLE_CREDENTIALS_JSON

Value: {"type":"service_account","project_id":"my-project-123","private_key_id":"abc123","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ...\n-----END PRIVATE KEY-----\n","client_email":"my-service@my-project.iam.gserviceaccount.com","client_id":"123456","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/..."}
```

## Important Notes

✅ **DO:**
- Copy the ENTIRE file contents
- Include all brackets `{` and `}`
- Keep all quotes as they are
- Include the private key (it's encrypted/secure)

❌ **DON'T:**
- Don't modify the JSON
- Don't add extra quotes around it
- Don't remove any fields
- Don't break it into multiple lines (unless Render supports multiline)

## Troubleshooting

### Error: "Failed to parse GOOGLE_CREDENTIALS_JSON"

**Solution:**
- Make sure you copied the ENTIRE JSON file
- Check that all brackets are included
- Verify there are no extra quotes at the start/end
- Try pasting it into a JSON validator: https://jsonlint.com

### Error: "Invalid credentials"

**Solution:**
- Verify the service account has **Cloud Translation API** enabled
- Check that the service account has proper permissions
- Ensure the JSON file is complete (not truncated)

### Error: "Authentication failed"

**Solution:**
- Verify the project ID is correct
- Check that Cloud Translation API is enabled in your Google Cloud project
- Ensure the service account email is correct

## Alternative: Using File Path (Local Development Only)

For **local development**, you can use a file path instead:

1. Keep the JSON file in your project (e.g., `credentials/vertex-key.json`)
2. Set environment variable: `GOOGLE_APPLICATION_CREDENTIALS=credentials/vertex-key.json`

**But for Render deployment, you MUST use `GOOGLE_CREDENTIALS_JSON` with the JSON string.**

## Still Having Issues?

1. **Verify your JSON is valid:**
   - Copy it to https://jsonlint.com
   - It should validate without errors

2. **Check Render logs:**
   - Go to your service → Logs
   - Look for error messages about credentials

3. **Test locally first:**
   - Set up `GOOGLE_APPLICATION_CREDENTIALS` locally
   - Verify translation works
   - Then use the same JSON content for Render

---

## Quick Reference

1. Get JSON file from Google Cloud Console
2. Open file → Select All → Copy
3. Render → Environment → Add `GOOGLE_CREDENTIALS_JSON`
4. Paste entire JSON content
5. Save → Service restarts automatically

That's it! 🎉

