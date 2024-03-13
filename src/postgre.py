from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.identity import AzureCliCredential
from src.util.logger import Logger

log = Logger.get_logger(__name__)

tenant_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'


def get_tag_value(postgre, tag):
    tags_default_value =  {'azuretag.start': '07:00', 
                           'azuretag.stop': '19:00' } 
    
    tags = postgre.tags
    return_value = None

    if tags and tag in tags:
        return_value = tags[tag]
    elif tag in tags_default_value:  
        return_value = tags_default_value[tag]

    return return_value                         
    

def get_postgres(credential,subscription_obj):
    subscription_name = subscription_obj.display_name.lower()
    log.info("Inicio da criacao do PostgreSQLManagementClient com a subscription " + subscription_name)
    try:
        compute_client = PostgreSQLManagementClient(credential=credential, subscription_id=subscription_obj.subscription_id)
        log.info("PostgreSQLManagementClient criado com sucesso com a subscription " + subscription_name)
    except Exception as e:
        log.info(f"Erro ao criar PostgreSQLManagementClient: {e}")  
    lista = compute_client.servers.list()
    
    subscription_postgres = []

    if 'landingzone' in subscription_name or 'name br dev' in subscription_name or 'name br non-prod' in subscription_name  or 'analytics' in subscription_name:
        lista = compute_client.servers.list()

        for postgre in lista:
            if (postgre.tags is not None 
                and 'azuretag.environment' in postgre.tags
                and 'azuretag.start' in postgre.tags
                and 'azuretag.stop' in postgre.tags
                and (
                        postgre.tags['azuretag.environment'] == 'dev'
                        or postgre.tags['azuretag.environment'] == 'stg'
                        or postgre.tags['azuretag.environment'] == 'nonprod'
                    )
                ): 
                subscription_postgres.append(postgre)

    return subscription_postgres

def ligar_postgre(credential,subscription_obj, postgre):
    compute_client = PostgreSQLManagementClient(credential=credential, subscription_id=subscription_obj.subscription_id)   
    resource_id_split = postgre.id.split('/')
    resourcegroup = resource_id_split[4].lower() 
    try:
        compute_client.servers.begin_start(resourcegroup, postgre.name)
        log.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> | StartingPostgres | <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        log.info("Starting postgres: " + postgre.name + " | Subscription: " + subscription_obj.display_name)
    except Exception as e:
        log.exception("Error: " + str(e))

def desligar_postgre(credential,subscription_obj, postgre):
    compute_client = PostgreSQLManagementClient(credential=credential, subscription_id=subscription_obj.subscription_id)
    resource_id_split = postgre.id.split('/')
    resourcegroup = resource_id_split[4].lower() 
    try:
        compute_client.servers.begin_stop(resourcegroup, postgre.name)
        log.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> | StoppingPostgres | <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        log.info("Stopping postgres: " + postgre.name + " | Subscription: " + subscription_obj.display_name)
    except Exception as e:
        log.exception("Error: " + str(e))
