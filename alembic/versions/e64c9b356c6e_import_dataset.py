"""import dataset

Revision ID: e64c9b356c6e
Revises: b369d098e7ce
Create Date: 2025-05-11 16:38:08.708278

"""
from typing import Sequence, Union
import os
import csv
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e64c9b356c6e'
down_revision: Union[str, None] = 'b369d098e7ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    connection = op.get_bind()
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../database.csv"))

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            connection.execute(
                sa.text("""
                    INSERT INTO sets (set_number, name, year_released, number_of_parts, theme_name)
                    VALUES (:set_number, :name, :year_released, :number_of_parts, :theme_name)
                """),
                {
                    "set_number": row["set_number"],
                    "name": row["name"],
                    "year_released": int(row["year_released"]),
                    "number_of_parts": int(row["number_of_parts"]),
                    "theme_name": row["theme_name"]
                }
            )

def downgrade():
    op.execute("DELETE FROM sets")