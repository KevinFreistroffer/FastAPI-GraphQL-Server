# from graphql_api.users.types import type_defs as user_type_defs
# from graphql_api.users.resolvers import user as user_resolvers, query as user_query_resolvers
from graphql_api.types import types
from graphql_api.resolvers import resolvers
from graphql_api.mutations import mutations
from ariadne.asgi import GraphQL
from ariadne import ObjectType, gql, make_executable_schema, load_schema_from_path

schema = make_executable_schema(types, resolvers, mutations)