from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # extra - allows to configure extra settings in model serializer
        # used to ensure that the password is right with the complexity rules
        extra_kwargs = {'password': {'write_only': True, 'min_length': 1}}

    # see django rest_framework docs
    # when we create the user django restframework will call this create
    # function and it will pass in the validated data that will contain all
    # the data that was passed into our serializer which would be json data
    # that was made in a http post. And it passes it as the as the argument
    # here and then we can use that to query
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    # instance is the model instance that is linked to our model serializer, is
    # the user object
    # validated_data are these fields that have been through the validation and
    # are ready to update
    def update(self, instance, validated_data):
        """Update a user setting the password correctly an return it"""

        # remove the password from the validated data
        # None - pop function requires a default value
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        # we want to make sure the password is set using the set_password
        # function instead of just setting it to whichever value is provided
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    # modify it slightly for to accept our email address instead of username
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validade and authenticate the user"""
        # attrs - contains every field that makes up our serializer
        email = attrs.get('email')
        password = attrs.get('password')

        # it passes the context in to the serializer in this context
        # and we can get a hold of the request that was made
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # it raises the validation and django rest framework knows how to
            # handle this and who handles it by passing the error as a 400
            # response and sending a response to the user which describes
            # this message
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
