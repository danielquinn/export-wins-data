from rest_framework import serializers

from .models import Win, Breakdown, Advisor, CustomerResponse, Notification


class WinSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)

    class Meta(object):
        model = Win
        fields = (
            "id",
            "user",
            "company_name",
            "cdms_reference",
            "customer_name",
            "customer_job_title",
            "customer_email_address",
            "customer_location",
            "business_type",
            "description",
            "name_of_customer",
            "name_of_export",
            "date",
            "country",
            "type",
            "total_expected_export_value",
            "goods_vs_services",
            "total_expected_non_export_value",
            "sector",
            "is_prosperity_fund_related",
            "hvo_programme",
            "has_hvo_specialist_involvement",
            "is_e_exported",
            "type_of_support_1",
            "type_of_support_2",
            "type_of_support_3",
            "associated_programme_1",
            "associated_programme_2",
            "associated_programme_3",
            "is_personally_confirmed",
            "is_line_manager_confirmed",
            "lead_officer_name",
            "lead_officer_email_address",
            "other_official_email_address",
            "line_manager_name",
            "team_type",
            "hq_team",
            "location",
            "created",
        )

    def validate_user(self, value):
        return self.context["request"].user


class LimitedWinSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    type = serializers.CharField(source="get_type_display")
    country = serializers.CharField(source="country.name")
    customer_location = serializers.CharField(source="get_customer_location_display")
    goods_vs_services = serializers.CharField(source="get_goods_vs_services_display")

    class Meta(object):
        model = Win
        fields = (
            "id",
            "description",
            "type",
            "date",
            "country",
            "customer_location",
            "total_expected_export_value",
            "total_expected_non_export_value",
            "goods_vs_services",
            "created",
        )


class BreakdownSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Breakdown
        fields = (
            "win",
            "type",
            "year",
            "value"
        )


class AdvisorSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Advisor
        fields = (
            "name",
            "team_type",
            "hq_team",
            "location"
        )


class NotificationSerializer(serializers.ModelSerializer):

    recipient = serializers.EmailField(required=False)

    class Meta(object):
        model = Notification
        fields = (
            "win",
            "user",
            "recipient",
            "type",
            "created"
        )


class CustomerResponseSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = CustomerResponse
        fields = (
            "win",
            "our_support",
            "access_to_contacts",
            "access_to_information",
            "improved_profile",
            "gained_confidence",
            "developed_relationships",
            "overcame_problem",
            "involved_state_enterprise",
            "interventions_were_prerequisite",
            "support_improved_speed",
            "expected_portion_without_help",
            "last_export",
            "company_was_at_risk_of_not_exporting",
            "has_explicit_export_plans",
            "has_enabled_expansion_into_new_market",
            "has_increased_exports_as_percent_of_turnover",
            "has_enabled_expansion_into_existing_market",
            "case_study_willing",
            "comments",
            "name",
            "created",
        )
