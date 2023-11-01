from django.shortcuts import render, get_object_or_404

# Inclui a classe HttpResponse
from django.http import HttpResponse

from django.views.generic import DetailView, ListView, TemplateView

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from blog.models import Post
from blog.forms import PostModelForm

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class PostDetailView(DetailView):
    model = Post
    template_name = "post/detail.html"
    context_object_name = "post"


def post_show(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "post/detail.html", {"post": post})


# Define uma function view chamada index
@login_required
def index(request):
    # return HttpResponse('Olá Django - index')
    return render(request, "index.html", {"titulo": "Últimos Artigos"})


# Define uma function view chamada ola.
def ola(request):
    # return HttpResponse('Olá Django')
    # return render(request, 'index.html')
    # return render(request, 'home.html')
    posts = Post.objects.all()  # recupera todos os posts do banco de dados
    context = {"posts_list": posts}  # cria um dicionário com os dado
    return render(
        request, "posts.html", context
    )  # renderiza o template e passa o contexto


def get_all_posts(request):
    posts = list(Post.objects.values("pk", "body_text", "pub_date"))
    data = {"success": True, "posts": posts}
    json_data = json.dumps(data, indent=1, cls=DjangoJSONEncoder)
    response = HttpResponse(json_data, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"  # requisição de qualquer origem
    return response


def get_post(request, post_id):
    post = Post.objects.filter(pk=post_id).values("pk", "body_text", "pub_date").first()

    data = {"success": True, "post": post}
    status = 200
    if post is None:
        data = {"success": False, "error": "Post ID não existe."}
        status = 404
    response = HttpResponse(
        json.dumps(data, indent=1, cls=DjangoJSONEncoder),
        content_type="application/json",
        status=status,
    )
    response["Access-Control-Allow-Origin"] = "*"  # requisição de qualquer origem
    return response


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post/post_form.html"
    success_url = reverse_lazy("posts_all")
    form_class = PostModelForm
    success_message = "Postagem salva com sucesso."

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostCreateView, self).form_valid(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"


class SobreTemplateView(TemplateView):
    template_name = "post/sobre.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post/post_form.html"
    success_url = reverse_lazy("posts_all")
    form_class = PostModelForm
    success_message = "Postagem salva com sucesso."

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, self.success_message)
        return super(PostUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context["form_title"] = "Criando um post"
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post/post_form.html"
    success_url = reverse_lazy("posts_all")
    form_class = PostModelForm
    success_message = "Postagem salva com sucesso."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(PostUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context["form_title"] = "Editando o post"
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post/post_confirm_delete_form.html"
    success_url = reverse_lazy("posts_all")
    success_message = "A postagem foi excluída com sucesso."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).form_valid(form)


@csrf_exempt
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        body_text = data.get("body_text")
        if body_text is None:
            data = {"success": False, "error": "Texto do post inválido."}
            status = 400  # Bad Request => erro do client
        else:
            post = Post(body_text=body_text)
            post.save()
            post_data = (
                Post.objects.filter(pk=post.id)
                .values("pk", "body_text", "pub_date")
                .first()
            )
            data = {"success": True, "post": post_data}
            status = 201  # Created
        response = HttpResponse(
            json.dumps(data, indent=1, cls=DjangoJSONEncoder),
            content_type="application/json",
            status=status,
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response
