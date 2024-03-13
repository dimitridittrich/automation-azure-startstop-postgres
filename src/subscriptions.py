from azure.identity import EnvironmentCredential 
from azure.mgmt.resource.subscriptions import SubscriptionClient
import os

class subscription():
    def __init__(self):
        self._credential = EnvironmentCredential()
        self._subscription = SubscriptionClient(credential=self._credential)
        self.azure_tenants = [
                                "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                            ]

        
        self.azure_subscriptions =  [
                                        "name br dev", 
                                        "name br non-prod",
                                        "analytics",
                                        "brewzone"
                                    ]
        
        self.all_subscriptions = self.__get_azure_list()

    def get_subscriptions(self, id=None, display_name=None, use_azure_subscriptions=False):
        return_id = ""
        return_list = []

        if display_name is not None:
            display_name = display_name.strip().lower()

        if use_azure_subscriptions:
            subscription_list = (s for s in self.all_subscriptions if any(xs in s.display_name.lower() for xs in self.azure_subscriptions))
        else:
            subscription_list = self.all_subscriptions

        for subscription in subscription_list:
            if id is not None and subscription.subscription_id == id:
                return_id = subscription
                break
            if display_name is not None and subscription.display_name.lower() == display_name.lower():
                return_id = subscription
                break
            else:
                return_list.append(subscription)

        if return_id != "":
            return return_id
        else:
            return return_list

    def __set_tenants_subscriptions(self):
        for tenant in self.azure_tenants:
            self.all_subscriptions += self.__get_azure_list()

    def __get_azure_list(self):
        subscription_client = self._subscription
        subscriptions = subscription_client.subscriptions.list()

        return subscriptions