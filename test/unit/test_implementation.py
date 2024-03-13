import unittest
from unittest.mock import patch, MagicMock
from src.implementation import StartStopPostgres

class TestStartStopPostgres(unittest.TestCase):

    @patch('src.implementation.subscription')
    @patch('src.implementation.get_postgres')
    @patch('src.implementation.get_tag_value')
    @patch('src.implementation.ligar_postgre')
    @patch('src.implementation.desligar_postgre')
    def test_startstop(self, mock_desligar_postgre, mock_ligar_postgre, mock_get_tag_value, mock_get_postgres, mock_subscription):
        mock_subscription_instance = mock_subscription.return_value
        mock_subscription_instance.get_subscriptions.return_value = []

        mock_postgres_instance = mock_get_postgres.return_value
        mock_postgres_instance.return_value = []

        mock_tag_value = mock_get_tag_value.return_value
        mock_tag_value.split.return_value = ["", ""]

        startstop_instance = StartStopPostgres()

        startstop_instance.startstop()

        mock_subscription_instance.get_subscriptions.assert_called_once()

if __name__ == '__main__':
    unittest.main()
