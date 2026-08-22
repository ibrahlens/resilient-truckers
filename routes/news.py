from flask import Blueprint, render_template

from models import News

news_bp = Blueprint(
    "news",
    __name__
)


# =====================================
# News List
# =====================================

@news_bp.route("/news")
def news():

    articles = (
        News.query
        .order_by(News.created_at.desc())
        .all()
    )

    return render_template(
        "news.html",
        articles=articles
    )


# =====================================
# Single Article
# =====================================

@news_bp.route("/news/<int:id>")
def article(id):

    article = News.query.get_or_404(id)

    return render_template(
        "article.html",
        article=article
    )