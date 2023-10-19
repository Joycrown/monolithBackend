from storages.backends.azure_storage import AzureStorage
# Azure configuration secret key --- GG6bWpYonhrHekFgSDqEq7T86q8yCEEB4q/gt0hSwQ3WH8AW
class AzureMediaStorage(AzureStorage):
    account_name = 'monolithteststorage' # Must be replaced by your <storage_account_name>
    account_key = '3mROEAnuUtkPJfAp1uNt0p9mDjpfHnp7Din89fb3hwy0az2HChMiKwK1dwDzYDRcNQgkDgzm5ljA+AStMvJsVw==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'monolithteststorage' # Must be replaced by your storage_account_name
    account_key = '3mROEAnuUtkPJfAp1uNt0p9mDjpfHnp7Din89fb3hwy0az2HChMiKwK1dwDzYDRcNQgkDgzm5ljA+AStMvJsVw==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
