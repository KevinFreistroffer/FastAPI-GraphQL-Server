from ariadne import MutationType
from graphql_api.resolvers.user import resolve_create_user, resolve_update_user

mutation = MutationType()
mutation.set_field("create_user", resolve_create_user)
mutation.set_field("update_user", resolve_update_user)
