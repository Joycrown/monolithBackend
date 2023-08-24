from storages.backends.azure_storage import AzureStorage
# Azure configuration secret key --- GG6bWpYonhrHekFgSDqEq7T86q8yCEEB4q/gt0hSwQ3WH8AW
class AzureMediaStorage(AzureStorage):
    account_name = 'pyramidteststorage' # Must be replaced by your <storage_account_name>
    account_key = 'okxqbWoC3SV/D0Q7ovXErdq5b5nrncyZhOT0cUJ2xRj1Z7i5IGdZAuOdTvdtQv3cI0oVf/TtVGgM+AStb64IbQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'pyramidteststorage' # Must be replaced by your storage_account_name
    account_key = 'okxqbWoC3SV/D0Q7ovXErdq5b5nrncyZhOT0cUJ2xRj1Z7i5IGdZAuOdTvdtQv3cI0oVf/TtVGgM+AStb64IbQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None