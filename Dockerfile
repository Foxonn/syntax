FROM python

EXPOSE 8080:80

COPY ./ /syntax/

RUN pip install pipenv

WORKDIR syntax

RUN pipenv install --deploy --system --ignore-pipfile

CMD uvicorn app:app --port 80 --host 0.0.0.0 --reload