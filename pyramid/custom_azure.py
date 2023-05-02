from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'pyramidstorages' # Must be replaced by your <storage_account_name>
    account_key = 'EveWBFoHTXyWtXIY2oiWvovoNpGvffWhahCa5/k20rlIV2Y8Px+svzlV9PNleF2OtCHYi015viO9+ASt4s/f9w==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'pyramidstorages' # Must be replaced by your storage_account_name
    account_key = 'EveWBFoHTXyWtXIY2oiWvovoNpGvffWhahCa5/k20rlIV2Y8Px+svzlV9PNleF2OtCHYi015viO9+ASt4s/f9w==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None