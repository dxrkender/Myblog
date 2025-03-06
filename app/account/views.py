# -*- coding: UTF-8 -*-
"""Add endpoints for url `/account` in path."""
from typing import Any

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from app.account.forms import (
    AccountLoginForm,
    AccountPasswordResetFrom,
    AccountProfileUpdateForm,
    AccountSetPasswordForm,
    AccountSignUpForm,
)
from app.account.models import Account
from app.account.tasks import send_reset_password_email


class AccountLoginView(LoginView):
    """Display the login form and handle the login action."""

    authentication_form = AccountLoginForm
    success_url = reverse_lazy("core:index")
    template_name = "account/login.html"
    redirect_authenticated_user = reverse_lazy("core:index")

    def get_context_data(self, **kwargs):
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Log in"
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        """Build the keyword arguments required to instantiate the form.

        Returns:
             Keyword arguments.
        """
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class AccountLogoutView(LogoutView):
    """Log out the user and redirect to the index page."""

    next_page = reverse_lazy("core:index")


class AccountSingUpView(CreateView):
    """Create a new user and redirect to the index page."""

    form_class = AccountSignUpForm
    success_url = reverse_lazy("account:login")
    template_name = "account/signup.html"

    def get(
        self,
        request: HttpRequest, *args, **kwargs,
    ) -> HttpResponseRedirect | HttpResponse:
        """Handle GET requests.

        If the user is logged in, redirect to the index page,
        creating and submitting the form otherwise.

        Args:
            request (HttpRequest): Request object.
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.

        Returns:
            Redirect to the index page if the user is logged in
            or render sing app page.
        """
        if request.user.is_authenticated:
            return redirect(reverse_lazy("core:index"))
        return render(
            request=request,
            template_name=self.template_name,
            context={"form": AccountSignUpForm()},
        )

    def get_context_data(self, **kwargs):
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign Up"
        return context


class AccountProfileDetailView(DetailView):
    """Render a "detail" view of an account."""

    model = Account
    context_object_name = "profile"
    template_name = "account/profile_detail.html"

    def get_context_data(self, **kwargs):
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Profile Details {self.request.user.username}"
        return context


class AccountProfileUpdateView(UpdateView):
    """Update an account's profile."""

    model = Account
    form_class = AccountProfileUpdateForm
    context_object_name = "profile"
    template_name = "account/profile_edit.html"

    def get_object(self, queryset: QuerySet = None):
        """Return the single object that this view will display.

        Args:
            queryset (QuerySet): If queryset is provided, that queryset
                will be used as the source of objects

        Returns:
            User instance.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """Add title and user in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Profile {self.request.user.username}"
        if self.request.method == "POST":
            context["form"] = AccountProfileUpdateForm(
                data=self.request.POST,
                instance=self.request.user,
            )
        else:
            context["form"] = AccountProfileUpdateForm(
                instance=self.request.user,
            )
        return context


class AccountPasswordResetView(PasswordResetView):
    """Send the mail."""

    form_class = AccountPasswordResetFrom
    template_name = "account/password_reset.html"
    email_template_name = "account/password_reset_email.html"
    success_url = reverse_lazy("account:password_reset_done")

    def form_valid(self, form) -> HttpResponseRedirect:
        """If the form is valid, redirect to the supplied URL.

        Args:
            form (AccountPasswordResetFrom): Cleared form instance.

        Returns:
            Redirect to the `success_url` variable in class attributes.
        """
        email = form.cleaned_data.get("email")
        send_reset_password_email.delay(email)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Password reset"
        return context


class AccountPasswordResetDoneView(PasswordResetDoneView):
    """Show a success message for the above."""

    template_name = "account/password_reset_done.html"

    def get_context_data(self, **kwargs):
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Password Reset Done"
        return context


class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    """Check the link the user clicked and prompts for a new password."""

    template_name = "account/password_reset_confirm.html"
    form_class = AccountSetPasswordForm
    success_url = reverse_lazy("account:password_reset_complete")

    def get_context_data(self, **kwargs):
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Password Reset Confirm"
        return context


class AccountPasswordResetCompleteView(PasswordResetCompleteView):
    """Show a success message for the above."""

    template_name = "account/password_reset_complete.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add title in the context data.

        Merge the context data of all parent classes with those of
        the current class.

        Args:
            **kwargs (dict): Some context variables.

        Returns:
            context (dict[str, Any]): Dictionary of context variables.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Password Reset Complete"
        return context
