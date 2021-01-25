from django import forms
from django.forms.widgets import HiddenInput

from .models import *


class GroupChatAddMemberForm(forms.ModelForm):
    inviter = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput()
    )
    invitee = forms.ModelChoiceField(
        queryset=User.objects.all(),
    )
    groupchatbox = forms.ModelChoiceField(
        queryset=GroupChatBox.objects.all(),
        widget=HiddenInput()
    )
    class Meta:
        model = JoinGroupChat
        fields = ['invitee', 'inviter', 'groupchatbox',]