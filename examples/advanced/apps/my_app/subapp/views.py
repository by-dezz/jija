from jija import views, response


class IndexView(views.View):
    def get(self):
        return response.Response(body='Hello, world!')
