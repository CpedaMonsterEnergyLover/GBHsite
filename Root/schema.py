import graphene

import GameObjects.schema as game_objects_schema


class Query(
    game_objects_schema.GameObjectsQuery,
):
    pass


schema = graphene.Schema(query=Query)
