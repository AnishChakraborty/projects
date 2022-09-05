from django_filters import CharFilter, FilterSet

class DoctorFilter(FilterSet):

    city = CharFilter(label="location", field_name="address", lookup_expr="icontains")
    specility = CharFilter(
        label="speciality", field_name="specility", lookup_expr="icontains"
    )
    name = CharFilter(
        label="NAME", field_name="user__firstname", lookup_expr="icontains"
    )
    fees_gt = CharFilter(label="fees_greater_than", field_name="fees", lookup_expr="gt")
    fees = CharFilter(label="fees_less_than", field_name="fees", lookup_expr="lt")
