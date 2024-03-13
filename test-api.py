import azure.mgmt.resource
import requests
import automationassets
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD
from datetime import datetime

def get_token(runas_connection, resource_url, authority_url):
    """ Returns credentials to authenticate against Azure resoruce manager """
    from OpenSSL import crypto
    from msrestazure import azure_active_directory
    import adal

    # Get the Azure Automation RunAs service principal certificate
    cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
    pks12_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pks12_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection["CertificateThumbprint"]
    tenant_id = runas_connection["TenantId"]

    # Authenticate with service principal certificate
    authority_full_url = (authority_url + '/' + tenant_id)
    context = adal.AuthenticationContext(authority_full_url)
    return context.acquire_token_with_client_certificate(
            resource_url,
            application_id,
            pem_pkey,
            thumbprint)['accessToken']

action = 'start'
""" day_of_week = datetime.today().strftime('%A')
if day_of_week == 'Saturday':
    action = 'stop'
elif day_of_week == 'Monday':
    action = 'start' """

subscription_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
resource_group = 'Test-Start-Stop-PostgreSQLFlexible'
server_name = 'test-postgresql-fs'

if action: 
    #print 'Today is ' + day_of_week + '. Executing ' + action + ' server'
    print('. Executing ' + action + ' server')
    runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
    resource_url = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id
    authority_url = AZURE_PUBLIC_CLOUD.endpoints.active_directory
    resourceManager_url = AZURE_PUBLIC_CLOUD.endpoints.resource_manager
    auth_token=get_token(runas_connection, resource_url, authority_url)
    url = 'https://management.azure.com/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + '/providers/Microsoft.DBforPostgreSQL/flexibleServers/' + server_name + '/' + action + '?api-version=2020-02-14-preview'
    response = requests.post(url, json={}, headers={'Authorization': 'Bearer ' + auth_token})
    print(response.json())
else: 
    #print 'Today is ' + day_of_week + '. No action taken'
    print('No action taken')