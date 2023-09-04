from azure.keyvault.secrets import SecretClient

class KeyVaultAPI:

    def __init__(self, key_vault_name, credential):
            key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
            self.client = SecretClient(vault_url=key_vault_url, credential=credential)


    def get_secret(self, secret_name):
        secret = self.client.get_secret(secret_name)
        return secret.value

if __name__ == "__main__":
    pass