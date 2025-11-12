# ---- build ----
FROM eclipse-temurin:17-jdk AS build
LABEL authors="Loogika"
WORKDIR /app
COPY . .
RUN ./gradlew --no-daemon clean bootJar

# ---- run ----
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
