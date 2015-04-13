"""Package with forms using in gallery pages.

Modules within:
albums -- forms for manipulations with albums.
common -- different service forms.
pictures -- forms for managing images.
users -- forms for providing user-related features.
"""

from pagapp.forms.albums import AlbumForm, AddAlbumForm, EditAlbumNameForm,\
    EditAlbumDescriptionForm, DeleteAlbumForm
from pagapp.forms.common import GotoUploadFakeForm
from pagapp.forms.pictures import PictureForm
from pagapp.forms.users import LoginForm, ChangePasswordForm


__all__ = ['albums', 'common', 'pictures', 'users']