# core/schema.py
from drf_spectacular.openapi import AutoSchema


class AppLabelAutoSchema(AutoSchema):
    def get_tags(self):
        module = self.view.__module__  # full dotted path
        parts = module.split(".")

        # common patterns:
        # project.apps.batches.views
        # apps.batches.views
        # batches.views

        if "apps" in parts:
            app_index = parts.index("apps") + 1
            return [parts[app_index].title()]

        if "views" in parts:
            return [parts[parts.index("views") - 1].title()]

        return super().get_tags()


class ViewNameAutoSchema(AutoSchema):
    def get_tags(self):
        # Use the ViewSet class name as the tag
        view_name = self.view.__class__.__name__

        # Remove "ViewSet" or "View"
        for suffix in ["ViewSet", "View"]:
            if view_name.endswith(suffix):
                view_name = view_name[: -len(suffix)]

        return [view_name]
