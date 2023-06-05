class SecurityController:
    def get_allowed_models(user):
        user_organisations = list(SecurityController.get_user_organisations(user))
        for user_organisation in user_organisations:
            for repository in user_organisation.repositories.all():
                for model in repository.repositories.all():
                    yield model

    def get_user_organisations(user):
        for profile in user.profiles.all():
             yield profile.organisation