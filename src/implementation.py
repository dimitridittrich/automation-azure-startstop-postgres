import src.env as envs
import datetime
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.identity import AzureCliCredential
from azure.core.exceptions import AzureError
from src.postgre import ligar_postgre, desligar_postgre, get_postgres, get_tag_value
from src.subscriptions import subscription
from src.util.logger import Logger


log = Logger.get_logger(__name__)


class StartStopPostgres():
    def startstop(self):
        hora_utc = datetime.datetime.utcnow()
        hora_atual = hora_utc + datetime.timedelta(hours=-3)
        hora_atual = hora_atual.hour

        azure_subscription = subscription()
        subscriptions = azure_subscription.get_subscriptions(use_azure_subscriptions=True)

        log.info("======================Subscriptions======================")
        for subscription_display in subscriptions:
            log.info(subscription_display.display_name)


        for subscription_obj in subscriptions:
            try:
                log.info("============================== Subscription: " + subscription_obj.display_name + " ==============================")
                log.info("Processing subscription: " + subscription_obj.display_name)
                postgres = get_postgres(azure_subscription._credential,subscription_obj=subscription_obj)

                for postgre in postgres:
                    log.info("Postgres name: " + postgre.name + " | Subscription: " + subscription_obj.display_name)

                    start = get_tag_value(postgre=postgre, tag='azuretag.start').split(":")[0]
                    stop = get_tag_value(postgre=postgre, tag='azuretag.stop').split(":")[0]

                    start_hour = int(start) if start.isdigit() else None
                    stop_hour = int(stop) if stop.isdigit() else None

                    dia_da_semana = datetime.datetime.today().weekday()

                    if dia_da_semana < 5:
                        if start_hour == hora_atual:
                            ligar_postgre(azure_subscription._credential,subscription_obj, postgre)
                    if stop_hour == hora_atual:
                        desligar_postgre(azure_subscription._credential,subscription_obj, postgre)
            except Exception as e:
                log.exception("Error: " + str(e))

    def run(self):
        log.info(f"Starting Postgres Start Stop")
        self.startstop()
