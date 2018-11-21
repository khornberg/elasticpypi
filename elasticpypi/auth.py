# modified from https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints/blob/master/blueprints/python/api-gateway-authorizer-python.py # noqa E501
import re


class HttpVerb:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    ALL = '*'


class AuthPolicy(object):
    awsAccountId = ''
    principalId = ''
    version = '2012-10-17'
    pathRegex = '^[/.a-zA-Z0-9-*]+$'
    allowMethods = []
    denyMethods = []
    restApiId = '*'
    region = '*'
    stage = '*'

    def __init__(self, principal, awsAccountId):
        self.awsAccountId = awsAccountId
        self.principalId = principal
        self.allowMethods = []
        self.denyMethods = []

    def _addMethod(self, effect, verb, resource, conditions):
        if verb != '*' and not hasattr(HttpVerb, verb):
            raise NameError('Invalid HTTP verb ' + verb + '. Allowed verbs in HttpVerb class')
        resourcePattern = re.compile(self.pathRegex)
        if not resourcePattern.match(resource):
            raise NameError('Invalid resource path: ' + resource + '. Path should match ' + self.pathRegex)

        if resource[:1] == '/':
            resource = resource[1:]
        resourceArn = 'arn:aws:execute-api:{}:{}:{}/{}/{}/{}'.format(
            self.region, self.awsAccountId, self.restApiId, self.stage, verb, resource
        )
        if effect.lower() == 'allow':
            self.allowMethods.append({
                'resourceArn': resourceArn,
                'conditions': conditions
            })
        elif effect.lower() == 'deny':
            self.denyMethods.append({
                'resourceArn': resourceArn,
                'conditions': conditions
            })

    def _getEmptyStatement(self, effect):
        statement = {
            'Action': 'execute-api:Invoke',
            'Effect': effect[:1].upper() + effect[1:].lower(),
            'Resource': []
        }
        return statement

    def _getStatementForEffect(self, effect, methods):
        statements = []
        if len(methods) > 0:
            statement = self._getEmptyStatement(effect)
            for curMethod in methods:
                if curMethod['conditions'] is None or len(curMethod['conditions']) == 0:
                    statement['Resource'].append(curMethod['resourceArn'])
                else:
                    conditionalStatement = self._getEmptyStatement(effect)
                    conditionalStatement['Resource'].append(curMethod['resourceArn'])
                    conditionalStatement['Condition'] = curMethod['conditions']
                    statements.append(conditionalStatement)
            if statement['Resource']:
                statements.append(statement)
        return statements

    def allowAllMethods(self):
        self._addMethod('Allow', HttpVerb.ALL, '*', [])

    def build(self):
        if ((self.allowMethods is None or len(self.allowMethods) == 0) and
                (self.denyMethods is None or len(self.denyMethods) == 0)):
            raise NameError('No statements defined for the policy')
        policy = {
            'principalId': self.principalId,
            'policyDocument': {
                'Version': self.version,
                'Statement': []
            }
        }
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect('Allow', self.allowMethods))
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect('Deny', self.denyMethods))
        return policy
