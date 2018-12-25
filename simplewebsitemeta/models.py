import hashlib
import metadata_parser

from django.db import models


class SimpleWebsiteMetaManager(models.Manager):
    def get_url(self, url, headers=None):
        hash_str = (hashlib.md5(url.encode('utf-8'))).hexdigest()

        # return from db if exists
        swm = SimpleWebsiteMeta.objects.filter(hash_str=hash_str).first()
        if swm is not None:
            return swm

        try:
            # run metadata_parser
            mdp = metadata_parser.MetadataParser(
                url=url,
                url_headers=headers,
                search_head_only=False,
                support_malformed=True
            )

            # retrieve our keys
            meta = {
                'description': mdp.get_metadatas('description'),
                'image': mdp.get_metadatas('image'),
                'title': mdp.get_metadatas('title'),
                'url': mdp.get_url_canonical()
            }
            for key in meta.keys():
                if type(meta[key]) is list:
                    meta[key] = meta[key][0]

            # save to db
            swm = SimpleWebsiteMeta(
                hash_str=hash_str,
                requested_url=url,
                description=meta['description'],
                image=meta['image'],
                title=meta['title'],
                canonical_url=meta['url']
            )
            swm.save()

            # return
            return swm
        except:
            return None


class SimpleWebsiteMeta(models.Model):
    hash_str = models.CharField(max_length=32, db_index=True)
    requested_url = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    canonical_url = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = SimpleWebsiteMetaManager()

    class Meta:
        ordering = ['-created']
