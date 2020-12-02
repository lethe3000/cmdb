from kubernetes import config
from kubernetes.client import ApiClient, Configuration


class KubeClient:
    api_client: ApiClient
    config: dict

    def new_client_from_dict(self, context: str) -> ApiClient:
        client_config = type.__call__(Configuration)
        config.load_kube_config_from_dict(config_dict=self.config, context=context, persist_config=False,
                                          client_configuration=client_config)
        return ApiClient(configuration=client_config)

    def __init__(self):

        pass
