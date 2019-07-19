from fbpost.models import *
from datetime import datetime
from django.db.models import *
from enum import Enum
from django.db import connection


class ReactionType(Enum):
    HAHA = "HAHA"
    WOW = "WOW"
    LIKE = "LIKE"
    LOVE = "LOVE"
    ANGRY = "ANGRY"
    SAD = "SAD"


def covert_datetime_object_to_string(posted_time):
    return posted_time.strftime("%Y-%m-%d %H:%M:%S.%f")


def convert_user_to_dict(user):
    return {"name": user.username, "user_id": user.id, "profile_pic_url": user.pic_url}


def covert_reaction_to_dict(reaction_queryset):
    list_of_reactions = []
    for reaction_object in reaction_queryset:
        list_of_reactions.append(reaction_object.react_type)
    reaction_dictionary = {"count": len(list_of_reactions), "type": list(set(list_of_reactions))}
    return reaction_dictionary


def create_user(username, pic_url):
    return User.objects.create(username=username, pic_url=pic_url)


def create_post(user_id, post_content):
    user = User.objects.get(id=user_id)
    post = Post.objects.create(post_datetime=covert_datetime_object_to_string(datetime.now()),
                               post_content=post_content, user=user)
    return post.id


def covert_comment_to_dict(comment):
    list_of_reply_dictionary = []
    comment_dictionary = {
        "comment_id": comment.id,
        "commenter": convert_user_to_dict(comment.commented_by),
        "commented_at": covert_datetime_object_to_string(comment.comment_at),
        "comment_content": comment.comment_content,
        'reactions': covert_reaction_to_dict(comment.reaction.all())
    }

    reply_query_set = comment.reply.all()
    for reply in reply_query_set:
        reply_dictionary = covert_comment_to_dict(reply)
        list_of_reply_dictionary.append(reply_dictionary)
    comment_dictionary["replies_count"] = len(list_of_reply_dictionary)
    comment_dictionary["replies"] = list_of_reply_dictionary
    return comment_dictionary


def get_post(post_id):
    post = Post.objects.select_related('user').prefetch_related('reaction',
                                                                    Prefetch('comments',
                                                                             queryset=Comment.objects.select_related(
                                                                                 'commented_by').prefetch_related(
                                                                                 'reaction').prefetch_related(
                                                                                 Prefetch('reply',
                                                                                          queryset=Comment.objects.select_related(
                                                                                              'commented_by').prefetch_related(
                                                                                              'reaction').prefetch_related(
                                                                                              'reply')))),
                                                                    ).get(id=post_id)

    return convert_post_to_post_dict(post)


def get_user_posts(user_id):
    try:
        User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("User Not Found")
    post_query_set = Post.objects.filter(user__id=user_id).select_related('user').prefetch_related('reaction',
                                                                                                   Prefetch('comments',
                                                                                                            queryset=Comment.objects.select_related(
                                                                                                                'commented_by').prefetch_related(
                                                                                                                'reaction').prefetch_related(
                                                                                                                Prefetch(
                                                                                                                    'reply',
                                                                                                                    queryset=Comment.objects.select_related(
                                                                                                                        'commented_by').prefetch_related(
                                                                                                                        'reaction').prefetch_related(
                                                                                                                        'reply')))),
                                                                                                   )
    list_of_user_posts = []
    for post in post_query_set:
        list_of_user_posts.append(convert_post_to_post_dict(post))
    return list_of_user_posts


def convert_post_to_post_dict(post):
    post_dictionary = {
        'post_id': post.id,
        'posted_by': convert_user_to_dict(post.user),
        'posted_at': covert_datetime_object_to_string(post.post_datetime),
        'post_content': post.post_content,
        'reactions': covert_reaction_to_dict(post.reaction.all())
    }

    comment_queryset = post.comments.all()
    list_of_comments_dictionary = []
    for comment in comment_queryset:
        comment_dictionary = covert_comment_to_dict(comment)
        list_of_comments_dictionary.append(comment_dictionary)

    post_dictionary["comments"] = list_of_comments_dictionary
    post_dictionary["comments_count"] = len(list_of_comments_dictionary)
    return post_dictionary


def delete_post(post_id):
    post = Post.objects.get(id=post_id)
    post.delete()


def react_to_post(user_id, post_id, reaction_type):
    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)
    if reaction_type not in [ReactionType.HAHA.value, ReactionType.LIKE.value, ReactionType.SAD.value,
                             ReactionType.WOW.value, ReactionType.LOVE.value]:
        raise Exception('Reaction DoesNotExist')

    try:
        reaction=Reactions.objects.get(user=user,post=post)
        if reaction_type == reaction.react_type:
            reaction.delete()
        elif reaction_type != reaction.react_type:
            reaction.react_type = reaction_type
            reaction.save()
    except Reactions.DoesNotExist:
        Reactions.objects.create(react_type=reaction_type, post=post,user=user)


def get_posts_reacted_by_user(user_id):
    try:
        User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("User Not Found")
        return
    list_of_post_ids = Post.objects.filter(reaction__user_id=user_id).values_list('id', flat=True)
    return list(list_of_post_ids)


def get_reactions_to_post(post_id):
    try:
        Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Post Not Found")
        return
    list_of_reactions = []
    reaction_query_set = Reactions.objects.filter(post_id=post_id).select_related('user')
    for reaction in reaction_query_set:
        user_dict = convert_user_to_dict(reaction.user)
        user_dict['reaction'] = reaction.react_type
        list_of_reactions.append(user_dict)
    return list_of_reactions


def get_reaction_metrics(post_id):
    try:
        Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Post Not Found")
        return
    reaction_dictionary = Reactions.objects.filter(post_id=post_id).values('react_type').annotate(
        reaction_count=Count('post'))
    reaction_metrics = {}
    for reaction in reaction_dictionary:
        reaction_metrics[reaction['react_type']] = reaction['reaction_count']
    return reaction_metrics


def get_posts_with_positive_reactions():
    return list(Post.objects.annotate(
        pos_count=Count('reaction', filter=Q(
            reaction__react_type__in=[ReactionType.LOVE.value, ReactionType.LIKE.value, ReactionType.HAHA.value,
                                      ReactionType.WOW.value])),
        neg_count=Count('reaction', filter=Q(
            reaction__react_type__in=[ReactionType.SAD.value, ReactionType.ANGRY.value]))).annotate(
        diff_count=F('pos_count') - F('neg_count')).filter(diff_count__gte=1).values_list('id', flat=True))


def add_comment(post_id, user_id, comment_text):
    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.create(commented_by=user, post=post,
                                     comment_at=covert_datetime_object_to_string(datetime.now()),
                                     comment_content=comment_text)
    return comment.id


def react_to_comment(user_id, comment_id, reaction_type):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Invalid User")
        return
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        print("Invalid Comment")
        return
    if reaction_type not in [ReactionType.HAHA.value, ReactionType.LIKE.value, ReactionType.SAD.value,
                             ReactionType.WOW.value, ReactionType.LOVE.value]:
        print("Reaction doesn't exist")
        return

    try:
        reaction = Reactions.objects.get(user_id=user_id, comment_id=comment_id)
    except Reactions.DoesNotExist:
        print("No Reaction Found")
        Reactions.objects.create(react_type=reaction_type, user=user, comment=comment)
        return
    if reaction_type == reaction.react_type:
        reaction.delete()
    else:
        reaction.react_type = reaction_type
        reaction.save()


def reply_to_comment(comment_id, user_id, reply_text):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Invalid User")
        return
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        print("Invalid Comment")
        return
    if comment.parent_comment is None:
        reply = Comment.objects.create(commented_by=user, comment_at=covert_datetime_object_to_string(datetime.now()),
                                       comment_content=reply_text)

    else:
        reply = Comment.objects.create(parent_comment=comment, commented_by=user,
                                       comment_at=covert_datetime_object_to_string(datetime.now()),
                                       comment_content=reply_text)

    return reply.id


def get_replies_for_comment(comment_id):
    try:
        comment = Comment.objects.select_related('commented_by').prefetch_related('reaction',
            Prefetch('reply', queryset=Comment.objects.select_related(
                'commented_by').prefetch_related(
                'reply'))).get(id=comment_id)
    except Comment.DoesNotExist:
        print("Invalid Comment")
        return
    list_of_reply_dictionary = covert_comment_to_dict(comment)
    list_of_reply_dictionary.pop('reactions', None)
    return list_of_reply_dictionary



