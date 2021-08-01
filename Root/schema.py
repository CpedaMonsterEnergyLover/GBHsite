import graphene

import GameObjects.schema as game_objects_schema
import Profiles.schema as group_query


class Query(
    game_objects_schema.GameObjectsQuery,
    group_query.GroupQuery
):
    pass


schema = graphene.Schema(query=Query)
