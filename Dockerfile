FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
CMD ["streamlit", "run", "app.py"]