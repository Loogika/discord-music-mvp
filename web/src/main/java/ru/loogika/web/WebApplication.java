package ru.loogika.web;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@SpringBootApplication
@RestController
public class WebApplication {

    @Value("${bot.url}")
    private String botUrl;

    private final HttpClient client = HttpClient.newHttpClient();

    public static void main(String[] args) {
        SpringApplication.run(WebApplication.class, args);
    }

    @PostMapping("/api/discord/send")
    public ResponseEntity<String> send(@RequestBody MessageBody body) {
        try {
            String msg = body.getMessage() != null ? body.getMessage() : "Hello from Java Web!";
            String json = String.format("{\"message\":\"%s\"}", msg);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(botUrl + "/send"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            client.send(request, HttpResponse.BodyHandlers.ofString());
            return ResponseEntity.ok("✅ Message sent: " + msg);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError()
                    .body("❌ Failed to send: " + e.getMessage());
        }
    }

    @GetMapping("/api/ping")
    public String ping() {
        return "pong";
    }

    public static class MessageBody {
        private String message;

        public String getMessage() {
            return message;
        }
        public void setMessage(String message) {
            this.message = message;
        }
    }
}
