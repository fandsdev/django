from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class AppJSONRenderer(CamelCaseJSONRenderer):
    charset = 'utf-8'  # force DRF to add charset header to the content-type
    json_underscoreize = {'no_underscore_before_number': True}  # https://github.com/vbabiy/djangorestframework-camel-case#underscoreize-options
