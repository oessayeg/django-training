from ex00.forms import LoginForm


def login_form_processor(request):
    if not request.user.is_authenticated:
        return {'login_form': LoginForm()}
    return {}

