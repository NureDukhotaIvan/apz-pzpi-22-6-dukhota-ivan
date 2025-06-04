from rest_framework import status
from rest_framework.response import Response

class ProfileDestroyMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        instance.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
