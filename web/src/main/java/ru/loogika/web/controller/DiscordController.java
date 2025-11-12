package ru.loogika.web.controller;

import java.net.URI;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;

import ru.loogika.web.config.BotProperties;
import ru.loogika.web.dto.SendMessageRequest;

@RestController
@RequestMapping("/api/discord")
public class DiscordController {

    private final RestTemplate restTemplate;
    private final URI sendUri;

    public DiscordController(RestTemplateBuilder restTemplateBuilder, BotProperties botProperties) {
        String baseUrl = Optional.ofNullable(botProperties.getUrl())
                .filter(StringUtils::hasText)
                .orElseThrow(() -> new IllegalStateException("Bot URL is not configured"));

        if (baseUrl.endsWith("/")) {
            baseUrl = baseUrl.substring(0, baseUrl.length() - 1);
        }

        this.sendUri = URI.create(baseUrl + "/send");
        this.restTemplate = restTemplateBuilder
                .setConnectTimeout(Duration.ofSeconds(5))
                .setReadTimeout(Duration.ofSeconds(30))
                .build();
    }

    @PostMapping("/send")
    public ResponseEntity<Map<String, Object>> sendMessage(@RequestBody(required = false) SendMessageRequest request) {
        Map<String, Object> payload = new HashMap<>();
        String message = request != null && request.getMessage() != null && !request.getMessage().isBlank()
                ? request.getMessage()
                : "Hello from API!";
        payload.put("message", message);

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(sendUri, payload, Map.class);
            Map<String, Object> body = response.getBody();
            if (body == null) {
                body = Map.of();
            }
            return ResponseEntity.status(response.getStatusCode()).body(body);
        } catch (RestClientResponseException ex) {
            Map<String, Object> errorBody = new HashMap<>();
            errorBody.put("status", "error");
            errorBody.put("detail", ex.getResponseBodyAsString());
            return ResponseEntity.status(ex.getStatusCode()).body(errorBody);
        } catch (RestClientException ex) {
            Map<String, Object> errorBody = new HashMap<>();
            errorBody.put("status", "error");
            errorBody.put("detail", ex.getMessage());
            return ResponseEntity.status(502).body(errorBody);
        }
    }
}
