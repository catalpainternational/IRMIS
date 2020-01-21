from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class CsvDataSource(models.Model):
    class Meta:
        unique_together = [["data_type", "path"]]

    data_type = models.CharField(max_length=24)
    path = models.TextField(
        help_text="The path inside the git@github.com:catalpainternational/estrada-data-sources.git repository"
    )
    added = models.DateTimeField(auto_now=True)
    columns = ArrayField(
        base_field=models.TextField(), help_text="The column names present in the csv"
    )


class CsvData(models.Model):
    source = models.ForeignKey(
        CsvDataSource, on_delete=models.CASCADE, related_name="rows"
    )
    row_index = models.PositiveSmallIntegerField(
        help_text="The row index from the source csv file"
    )
    data = JSONField()
