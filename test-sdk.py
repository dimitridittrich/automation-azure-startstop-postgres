from azure.identity import AzureCliCredential
#from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient

# Auth
tenant_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
subscription_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
resource_group = 'Test-Start-Stop-PostgreSQLFlexible'
server_name = 'test-postgresql-fs'

# Credentials
credentials = AzureCliCredential()
#credentials = DefaultAzureCredential()

# PostgreSQL Management Client
postgresql_client = PostgreSQLManagementClient(credentials, subscription_id)
print(postgresql_client)
print("======================")


# Stopping PostgreSQL Flexible
operation_stop = postgresql_client.servers.begin_stop(resource_group, server_name)

# Result Operation Stop
print(operation_stop)
print('A operação de "stop" foi iniciada com sucesso no PostgreSQL Flexible {server_name}!')

"""

# Starting PostgreSQL Flexible
operation_start = postgresql_client.servers.begin_start(resource_group, server_name)

# Result Operation Start
print(operation_start)
print('A operação de "start" foi iniciada com sucesso no PostgreSQL Flexible {server_name}!')
"""




