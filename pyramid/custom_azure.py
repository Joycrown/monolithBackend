from storages.backends.azure_storage import AzureStorage
# Azure configuration secret key --- GG6bWpYonhrHekFgSDqEq7T86q8yCEEB4q/gt0hSwQ3WH8AW
class AzureMediaStorage(AzureStorage):
    account_name = 'pyramidstorages' # Must be replaced by your <storage_account_name>
    account_key = 'GG6bWpYonhrHekFgSDqEq7T86q8yCEEB4q/gt0hSwQ3WH8AW/1CR+409dhHsX2+WFAA5mDUzDdRq+AStEflwKQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'pyramidstorages' # Must be replaced by your storage_account_name
    account_key = 'GG6bWpYonhrHekFgSDqEq7T86q8yCEEB4q/gt0hSwQ3WH8AW/1CR+409dhHsX2+WFAA5mDUzDdRq+AStEflwKQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None