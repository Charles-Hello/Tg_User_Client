
FROM ubuntu
WORKDIR /app
COPY .env tg_user  /app/
EXPOSE 8100 18535
ENV PYTHONIOENCODING=utf-8
CMD ["./tg_user"]