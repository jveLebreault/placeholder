from placeholder import load_config, CsvToDatabase, DatabaseNotSupportedError
import unittest
from configparser import ConfigParser

class CsvToDatabaseTest(unittest.TestCase):

    def test_initIncorrectDatabaseType(self):
        config_dict = {'database': {
            'type': 'my-not-supported-db-type'
        }}

        self.assertRaises(DatabaseNotSupportedError, CsvToDatabase, config_dict=config_dict)

    def test_placeholder(self):
        csvToDatabase = CsvToDatabase()
        print(csvToDatabase.csvFileList)




class LoadConfigTest(unittest.TestCase):

    def test_loadDefaultConfig(self):
        config = load_config()

        self.assertIsInstance(config, ConfigParser)
        self.assertEqual(config.get('database', 'type'), 'sqlite')
        self.assertEqual(config.get('database', 'user'), '')
        self.assertEqual(config.get('database', 'password'), '')


    def test_loadConfigFromDir(self):
        dir_path = './testconfig'
        config = load_config(dir_path)

        self.assertIsInstance(config, ConfigParser)
        self.assertEqual(config.get('database', 'type'), 'test')
        self.assertEqual(config.get('database', 'user'), 'test_user')
        self.assertEqual(config.get('database', 'password'), 'test_password')
        self.assertEqual(config.get('database', 'uri'), 'database@uri')
        self.assertEqual(config.get('csv', 'directories'), '/sample/directory')


    def test_loadConfigFile(self):
        file_path = './testconfig/testconfig.ini'     
        config = load_config(file_path)

        self.assertIsInstance(config, ConfigParser)
        self.assertEqual(config.get('database', 'type'), 'test')
        self.assertEqual(config.get('database', 'user'), 'test_user')
        self.assertEqual(config.get('database', 'password'), 'test_password')   


    def test_loadConfigFromDict(self):
        config_dict = {'database': {
            'user': 'dict_user',
            'password': 'password_user'
        }}
        
        config = load_config(config_dict=config_dict)
        self.assertEqual(config.get('database', 'user'), 'dict_user')
        self.assertEqual(config.get('database', 'password'), 'password_user')


if __name__ == '__main__':
    unittest.main()