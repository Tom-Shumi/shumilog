import logging
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        primary_msg = ''
        modal_primary_msg_show = 0
        if "pm" in request.GET:
            pm = request.GET.get("pm")
            if pm == '1':
                primary_msg = 'ユーザ登録が完了しました。'
                modal_primary_msg_show = 1

        context = {
            'modal_primary_msg_show': modal_primary_msg_show,
            'primary_msg': primary_msg
        }
        return self.render_to_response(context)


class MenuView(LoginRequiredMixin, generic.TemplateView):
    template_name = "menu.html"
