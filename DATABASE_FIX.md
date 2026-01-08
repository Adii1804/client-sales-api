# URGENT: Azure SQL Firewall Configuration Required

## Error: Login timeout expired

Your API is deployed successfully, but **cannot connect to the database** due to firewall restrictions.

## Solution Steps:

### 1. **Allow Azure Services to Access SQL Server**

**Azure Portal → SQL Server → Networking:**

1. Go to your Azure SQL Server (NOT the database)
2. Click **"Networking"** (or "Firewalls and virtual networks")
3. Under **"Exceptions"**, check:
   ✅ **"Allow Azure services and resources to access this server"**
4. Click **"Save"**

### 2. **Add App Service Outbound IPs (If above doesn't work)**

**Get App Service Outbound IPs:**
1. Go to Azure Portal → Your App Service → **Properties**
2. Copy all **"Outbound IP Addresses"**

**Add to SQL Server Firewall:**
1. Go to SQL Server → **Networking** → **Firewall rules**
2. Add each IP address as a firewall rule:
   - Name: `AppService-IP-1`
   - Start IP: `<outbound-ip>`
   - End IP: `<same-outbound-ip>`
3. Click **"Save"**

### 3. **Verify Environment Variables**

Make sure these are set in **App Service → Configuration → Application Settings**:

```
DB_USER = <your-sql-username>
DB_PASS = <your-sql-password>
DB_HOST = <yourserver>.database.windows.net
DB_PORT = 1433
DB_NAME = <your-database-name>
```

⚠️ **IMPORTANT:** After setting environment variables, click **"Save"** and then **"Restart"** the App Service.

### 4. **Test Connection**

After fixing the firewall, test your API:

```
https://client-sales-api.azurewebsites.net/docs
```

## Alternative: Use Private Endpoint (More Secure)

For production environments, consider:
- Azure SQL Private Endpoint
- VNet Integration for App Service
- No public internet access to database

## Quick Test Command

Once firewall is configured, test the API:

```powershell
# Login
$loginResponse = Invoke-RestMethod -Uri "https://client-sales-api.azurewebsites.net/auth/login" -Method POST -Body @{username="<API_USERNAME>"; password="<API_PASSWORD>"} -ContentType "application/x-www-form-urlencoded"

$token = $loginResponse.access_token

# Test sales endpoint
Invoke-RestMethod -Uri "https://client-sales-api.azurewebsites.net/sales/receipt-wise?from_date=2025-01-01&to_date=2025-01-01" -Headers @{Authorization="Bearer $token"}
```

## Summary

✅ App deployment: **SUCCESS**
✅ Gunicorn running: **SUCCESS**
✅ Authentication working: **SUCCESS**
❌ Database connection: **BLOCKED BY FIREWALL**

**Next Step:** Enable Azure SQL firewall rule as described above.
