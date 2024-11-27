from django import forms
from .models import Folder, UploadedFile

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_folder': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract 'user' from kwargs
        super(FolderForm, self).__init__(*args, **kwargs)
        
        # Filter the parent_folder field to only show folders of the current user
        if user:
            self.fields['parent_folder'].queryset = Folder.objects.filter(user=user)


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['folder', 'file']
        widgets = {
            'folder': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract 'user' from kwargs
        super(FileUploadForm, self).__init__(*args, **kwargs)
        
        # Filter the 'folder' field to show only folders belonging to the logged-in user
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(user=user)



