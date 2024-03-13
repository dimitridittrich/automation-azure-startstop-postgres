import unittest
from unittest.mock import Mock, patch
from src.subscriptions import subscription


class TestSubscription(unittest.TestCase):
    def setUp(self):
        self.mock_env_credential = Mock()
        self.mock_subscription_client = Mock()
        self.mock_subscription_list = [
            Mock(subscription_id="1", display_name="name br dev"),
            Mock(subscription_id="2", display_name="name br nonprod"),
            Mock(subscription_id="3", display_name="name br prd"),
        ]
        self.mock_subscription_client.subscriptions.list.return_value = (
            self.mock_subscription_list
        )

        patcher1 = patch(
            "src.subscriptions.EnvironmentCredential",
            return_value=self.mock_env_credential,
        )
        patcher2 = patch(
            "src.subscriptions.SubscriptionClient",
            return_value=self.mock_subscription_client,
        )
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)
        self.patcher1 = patcher1.start()
        self.patcher2 = patcher2.start()

    def test_get_subscriptions_by_display_name(self):
        sub = subscription()
        result = sub.get_subscriptions(display_name="name br dev")
        self.assertEqual(result.display_name, "name br dev")

    def test_get_subscriptions_by_id(self):
        sub = subscription()
        result = sub.get_subscriptions(id="1")
        self.assertEqual(result.display_name, "name br dev")

    def test_get_subscriptions_all(self):
        sub = subscription()
        result = sub.get_subscriptions(None, None)
        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()
