from rest_framework import serializers

from .models import Win, Breakdown, Advisor, CustomerResponse


class CustomerResponseSerializer(serializers.ModelSerializer):

    win_id = serializers.CharField(source="win__pk")

    class Meta(object):
        model = CustomerResponse
        fields = (
            "win_id",
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
            "comments",
            "name",
            "created",
        )


class WinSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)

    class Meta(object):
        model = Win
        fields = (
            "id",
            "company_name",
            "cdms_reference",
            "customer_name",
            "customer_job_title",
            "customer_email_address",
            "customer_location",
            "description",
            "type",
            "date",
            "country",
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
            "line_manager_name",
            "team_type",
            "hq_team",
            "location",
            "created",
        )


class LimitedWinSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)

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
