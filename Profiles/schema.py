import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Group, GroupHasMember


class GroupHasMemberType(DjangoObjectType):
    class Meta:
        model = GroupHasMember
        fields = ("name", "group", "date_joined", "role", "hero")


class GroupType(DjangoObjectType):
    members = DjangoListField(GroupHasMemberType)

    @graphene.resolve_only_args
    def resolve_members(self):
        return self.members.all()

    class Meta:
        model = Group
        fields = ("leader", "name", "date_created", "members",
                  "private", "min_level")


class GroupQuery(graphene.ObjectType):
    all_groups = DjangoListField(GroupType)
    group_by_id = graphene.Field(GroupType, id=graphene.Int(required=True))

    def resolve_all_groups(self, info):
        return Group.objects.all()

    def resolve_dice_by_id(self, info, id):
        try:
            return Group.objects.get(id=id)
        except Group.DoesNotExist:
            return None
