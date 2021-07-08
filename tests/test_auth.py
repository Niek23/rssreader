import pytest


class TestAuthAPI:
    @pytest.mark.django_db(transaction=True)

    def test_auth(self, client, user):

        response = client.post('/auth/token/login/',
                               data={'username': user.username, 'password': '1234567'})

        assert response.status_code != 404, \
            'Route `/auth/token/login/` is not found, check the route in *urls.py*'

        assert response.status_code == 200, \
            'Route `/auth/token/login/` does not return code 200'
        
        auth_data = response.json()
        assert 'auth_token' in auth_data, \
            'Make sure POST request `/auth/token/login/` returns auth_token'
