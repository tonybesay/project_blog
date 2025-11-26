from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.groups.filter(name=self.group_required).exists()

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta página.")
        return redirect("core:home")