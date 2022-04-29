# modified from https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints/blob/master/blueprints/python/api-gateway-authorizer-python.py # noqa E501
import re


class HttpVerb:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    ALL = "*"


class AuthPolicy(object):
    aws_account_id = ""
    principal_id = ""
    version = "2012-10-17"
    path_regex = "^[/.a-zA-Z0-9-*]+$"
    allow_methods = []
    deny_methods = []
    rest_api_id = "*"
    region = "*"
    stage = "*"

    def __init__(self, principal, aws_account_id):
        self.aws_account_id = aws_account_id
        self.principal_id = principal
        self.allow_methods = []
        self.deny_methods = []

    def _add_method(self, effect, verb, resource, conditions):
        if verb != "*" and not hasattr(HttpVerb, verb):
            raise NameError("Invalid HTTP verb " + verb + ". Allowed verbs in HttpVerb class")
        resources_pattern = re.compile(self.path_regex)
        if not resources_pattern.match(resource):
            raise NameError("Invalid resource path: " + resource + ". Path should match " + self.path_regex)

        if resource[:1] == "/":
            resource = resource[1:]
        resource_arn = "arn:aws:execute-api:{}:{}:{}/{}/{}/{}".format(
            self.region, self.aws_account_id, self.rest_api_id, self.stage, verb, resource
        )
        if effect.lower() == "allow":
            self.allow_methods.append({"resource_arn": resource_arn, "conditions": conditions})
        elif effect.lower() == "deny":
            self.deny_methods.append({"resource_arn": resource_arn, "conditions": conditions})

    def _get_empty_statement(self, effect):
        statement = {"Action": "execute-api:Invoke", "Effect": effect[:1].upper() + effect[1:].lower(), "Resource": []}
        return statement

    def _get_statement_for_effect(self, effect, methods):
        statements = []
        if len(methods) > 0:
            statement = self._get_empty_statement(effect)
            for current_method in methods:
                if current_method["conditions"] is None or len(current_method["conditions"]) == 0:
                    statement["Resource"].append(current_method["resource_arn"])
                else:
                    conditional_statement = self._get_empty_statement(effect)
                    conditional_statement["Resource"].append(current_method["resource_arn"])
                    conditional_statement["Condition"] = current_method["conditions"]
                    statements.append(conditional_statement)
            if statement["Resource"]:
                statements.append(statement)
        return statements

    def allow_all_methods(self):
        self._add_method("Allow", HttpVerb.ALL, "*", [])

    def build(self):
        if (self.allow_methods is None or len(self.allow_methods) == 0) and (
            self.deny_methods is None or len(self.deny_methods) == 0
        ):
            raise NameError("No statements defined for the policy")
        policy = {"principalId": self.principal_id, "policyDocument": {"Version": self.version, "Statement": []}}
        policy["policyDocument"]["Statement"].extend(self._get_statement_for_effect("Allow", self.allow_methods))
        policy["policyDocument"]["Statement"].extend(self._get_statement_for_effect("Deny", self.deny_methods))
        return policy
