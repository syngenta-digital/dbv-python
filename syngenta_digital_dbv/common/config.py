import json
import secrets

import boto3


class Config:

    def __init__(self, **kwargs):
        self.config = kwargs
        self.ssm_param = kwargs.get('ssm_param')
        self.seed = kwargs.get('seed', False)
        self.param_found = False
        self.random_password = secrets.token_urlsafe(16)
        self.reset_root = self.config.get('reset_root', False)
        self.config['password'] = self.config['password'] if not self.reset_root else self.random_password
        self.ssm = boto3.client('ssm')

    def get_config(self):
        config = self.__get_ssm_param()
        if config:
            return config
        return self.config

    def upload_config(self):
        if not self.param_found and self.ssm_param:
            self.ssm.put_parameter(
                Name=self.ssm_param,
                Type='SecureString',
                Value=json.dumps(self.config)
            )

    def __get_ssm_param(self):
        if self.ssm_param:
            try:
                result = self.ssm.get_parameter(Name=self.ssm_param, WithDecryption=True)
                ssm_config = json.loads(result['Parameter']['Value'])
            except self.ssm.exceptions.ParameterNotFound:
                return None
            except Exception as e:
                print(e)
                raise Exception from e
            else:
                self.param_found = True
                return ssm_config
        return None
