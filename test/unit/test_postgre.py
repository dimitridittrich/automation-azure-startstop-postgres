from unittest.mock import MagicMock, patch
import unittest
from src.postgre import get_tag_value, get_postgres, ligar_postgre, desligar_postgre
from azure.core.exceptions import AzureError

class TestPostgre(unittest.TestCase):
    def test_get_tag_value(self):
        mock_postgre = MagicMock()
        mock_postgre.tags = {'azuretag.environment': 'dev', 'azuretag.start': '07:00', 'azuretag.stop': '19:00'}
        result = get_tag_value(mock_postgre, 'azuretag.environment')
        self.assertEqual(result, 'dev')

    @patch('src.postgre.PostgreSQLManagementClient')
    def test_get_postgres_success(self, mock_client):
        mock_subscription = MagicMock()
        mock_subscription.display_name = 'landingzone'
        mock_subscription.subscription_id = 'test_subscription_id'

        mock_server1 = MagicMock()
        mock_server1.tags = {
            'azuretag.environment': 'dev',
            'azuretag.start': '07:00',
            'azuretag.stop': '19:00'
        }
        mock_server2 = MagicMock()
        mock_server2.tags = {
            'azuretag.environment': 'stg',
            'azuretag.start': '08:00',
            'azuretag.stop': '20:00'
        }
        mock_client_instance = mock_client.return_value
        mock_client_instance.servers.list.return_value = [mock_server1, mock_server2]

        result = get_postgres(MagicMock(), mock_subscription)

        self.assertEqual(len(result), 2)
        self.assertIn(mock_server1, result)
        self.assertIn(mock_server2, result)

    @patch('src.postgre.PostgreSQLManagementClient')
    def test_get_postgres_empty_server_list(self, mock_client):
        mock_subscription = MagicMock()
        mock_subscription.display_name = 'landingzone'
        mock_subscription.subscription_id = 'test_subscription_id'

        mock_client_instance = mock_client.return_value
        mock_client_instance.servers.list.return_value = []

        result = get_postgres(MagicMock(), mock_subscription)

        self.assertEqual(len(result), 0)

    @patch('src.postgre.PostgreSQLManagementClient')
    def test_get_postgres_no_matching_servers(self, mock_client):
        mock_subscription = MagicMock()
        mock_subscription.display_name = 'landingzone'
        mock_subscription.subscription_id = 'test_subscription_id'

        mock_server = MagicMock()
        mock_server.tags = {
            'azuretag.environment': 'prd',
            'azuretag.start': '07:00',
            'azuretag.stop': '19:00'
        }
        mock_client_instance = mock_client.return_value
        mock_client_instance.servers.list.return_value = [mock_server]

        result = get_postgres(MagicMock(), mock_subscription)

        self.assertEqual(len(result), 0)

    @patch('src.postgre.PostgreSQLManagementClient')
    def test_ligar_postgre(self, mock_client):
        mock_subscription_obj = MagicMock()
        mock_subscription_obj.display_name = 'test_subscription'
        mock_postgre_obj = MagicMock()
        credential = MagicMock() 
        
        ligar_postgre(credential, mock_subscription_obj, mock_postgre_obj)
        mock_client.return_value.servers.begin_start.assert_called_once()

    @patch('src.postgre.PostgreSQLManagementClient')
    def test_desligar_postgre(self, mock_client):
        mock_subscription_obj = MagicMock()
        mock_subscription_obj.display_name = 'test_subscription'
        mock_postgre_obj = MagicMock()
        credential = MagicMock() 
        
        desligar_postgre(credential, mock_subscription_obj, mock_postgre_obj)
        mock_client.return_value.servers.begin_stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()
