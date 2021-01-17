from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'data')
