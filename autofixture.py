from autofixture import AutoFixture
from qa.models import Answer

fixture = AutoFixture(Answer, generate_fk=True)
entries = fixture.create(57)
