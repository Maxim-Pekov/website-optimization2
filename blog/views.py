from django.shortcuts import render
from blog.models import Comment, Post, Tag
from django.db.models import Count


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count,
    }


def index(request):
    most_popular_posts = Post.objects.prefetch_popular_posts_with_comments_count_tags_author()[:5]
    most_fresh_posts = Post.objects.prefetch_related('author').annotate(comments_count=Count('comments')).prefetch_with_tags().order_by('-published_at')[:5:-1]
    most_popular_tags = Tag.objects.popular_tags()[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.select_related('author').popular_posts().get(slug=slug)
    comments = Comment.objects.select_related('post', 'author').filter(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.popular_tags()],
    }

    most_popular_tags = Tag.objects.popular_tags()[:5]
    most_popular_posts = Post.objects.prefetch_popular_posts_with_comments_count_tags_author()[:5]

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    popular_tags = Tag.objects.popular_tags().prefetch_related('posts')
    most_popular_tags = popular_tags[:5]

    tag = popular_tags.get(title=tag_title)

    related_posts = tag.posts.prefetch_posts_with_comments_count_tags_author()
    most_popular_posts = Post.objects.prefetch_popular_posts_with_comments_count_tags_author()[:5]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts[:20]],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})