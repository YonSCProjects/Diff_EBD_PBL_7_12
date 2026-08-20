// ============================================================
// Project 7 - Camera-Equipped Explorer
// Sketch 01: Camera + Drive (see and steer from the phone)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   The ESP32-CAM creates a Wi-Fi network. One page on the
//   phone shows LIVE VIDEO from the camera with driving
//   buttons underneath. You explore rooms you are not in.
//
// BOARD SETTINGS (different from the ESP32 of Project 5!):
//   Tools > Board > esp32 > "AI Thinker ESP32-CAM"
//   Upload happens through the FTDI programmer - see the card.
//
// POWER RULE (the most important line in this project):
//   The camera gets its OWN 5V from the small buck converter.
//   If the camera shares the motors' power it will keep
//   restarting ("brownout"). Motors from the L298N, camera
//   from the buck - always.
//
// DRIVING WITH 4 PINS:
//   The ESP32-CAM has few free pins, so the two speed jumpers
//   (ENA/ENB) STAY ON the L298N, and the sketch controls
//   speed by pulsing the direction pins themselves.
// ============================================================

#include "esp_camera.h"
#include <WiFi.h>
#include "esp_http_server.h"

// ---- YOUR EXPLORER'S NAME (English letters/numbers) ----
const char* CAR_WIFI_NAME = "EXPLORER-01";   // change 01 to your station number

// ---- SPEED (0-200 maximum! fresh batteries are strong) ----
const int SPEED      = 160;   // driving speed
const int TURN_SPEED = 140;   // pivot-turn speed

// ---- MOTOR PINS (the four free pins of the ESP32-CAM) ----
const int IN1 = 14;  // left side
const int IN2 = 15;  // left side
const int IN3 = 13;  // right side
const int IN4 = 12;  // right side
// ENA/ENB jumpers stay ON the L298N - speed comes from pulsing
// these four pins (PWM), not from separate speed pins.

// ---- CAMERA PINS (AI-Thinker ESP32-CAM - do not change) ----
#define PWDN_GPIO_NUM  32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM   0
#define SIOD_GPIO_NUM  26
#define SIOC_GPIO_NUM  27
#define Y9_GPIO_NUM    35
#define Y8_GPIO_NUM    34
#define Y7_GPIO_NUM    39
#define Y6_GPIO_NUM    36
#define Y5_GPIO_NUM    21
#define Y4_GPIO_NUM    19
#define Y3_GPIO_NUM    18
#define Y2_GPIO_NUM     5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM  23
#define PCLK_GPIO_NUM  22

httpd_handle_t web_httpd = NULL;
httpd_handle_t stream_httpd = NULL;

// ---- driving: PWM on the IN pins (8-bit, 5 kHz) ----
void setMotor(int pinFwd, int pinBack, int spd) {  // spd -200..200
  if (spd > 0)      { analogWrite(pinBack, 0);   analogWrite(pinFwd, spd); }
  else if (spd < 0) { analogWrite(pinFwd, 0);    analogWrite(pinBack, -spd); }
  else              { analogWrite(pinFwd, 0);    analogWrite(pinBack, 0); }
}
void driveLR(int left, int right) {
  setMotor(IN1, IN2, left);
  setMotor(IN3, IN4, right);
}
void stopCar() { driveLR(0, 0); }

// ---- the explorer page: live video + driving buttons ----
static const char PAGE[] = R"rawliteral(
<!DOCTYPE html><html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>הסייר שלי</title>
<style>
  body { margin:0; font-family:sans-serif; background:#0d1b2a; color:#fff;
         display:flex; flex-direction:column; align-items:center; min-height:100vh;
         -webkit-user-select:none; user-select:none; touch-action:manipulation; }
  h1 { font-size:1.15rem; margin:8px 0 6px; }
  img { width:96vw; max-width:640px; border-radius:12px; background:#000;
        aspect-ratio:4/3; object-fit:contain; }
  .pad { display:grid; grid-template-columns:76px 76px 76px; grid-gap:10px;
         justify-content:center; margin:12px 0 16px; }
  button { border:none; border-radius:16px; font-size:1.7rem; color:#fff;
           background:#2563eb; height:76px; }
  button:active { transform:translateY(3px); }
  .stop { background:#dc2626; font-size:1.1rem; font-weight:700; }
  .ghost { visibility:hidden; }
</style></head><body>
<h1>&#128247; הסייר שלי</h1>
<img id="cam" src="">
<div class="pad">
  <button class="ghost"></button>
  <button id="f">&#8679;</button>
  <button class="ghost"></button>
  <button id="r">&#8680;</button>
  <button class="stop" id="s">עצור</button>
  <button id="l">&#8678;</button>
  <button class="ghost"></button>
  <button id="b">&#8681;</button>
  <button class="ghost"></button>
</div>
<script>
  document.getElementById('cam').src =
    location.protocol + '//' + location.hostname + ':81/stream';
  function go(c){ fetch('/go?d='+c).catch(function(){}); }
  ['f','b','l','r'].forEach(function(id){
    var el = document.getElementById(id);
    el.addEventListener('pointerdown', function(e){ e.preventDefault(); go(id); });
    el.addEventListener('pointerup',   function(){ go('s'); });
    el.addEventListener('pointercancel', function(){ go('s'); });
    el.addEventListener('contextmenu', function(e){ e.preventDefault(); });
  });
  document.getElementById('s').addEventListener('pointerdown', function(){ go('s'); });
</script>
</body></html>
)rawliteral";

// ---- HTTP handlers ----
static esp_err_t page_handler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html; charset=utf-8");
  return httpd_resp_send(req, PAGE, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t go_handler(httpd_req_t *req) {
  char query[16] = {0};
  char d[4] = {0};
  httpd_req_get_url_query_str(req, query, sizeof(query));
  httpd_query_key_value(query, "d", d, sizeof(d));
  if      (d[0] == 'f') driveLR( SPEED,  SPEED);
  else if (d[0] == 'b') driveLR(-SPEED, -SPEED);
  else if (d[0] == 'l') driveLR(-TURN_SPEED,  TURN_SPEED);
  else if (d[0] == 'r') driveLR( TURN_SPEED, -TURN_SPEED);
  else                  stopCar();
  httpd_resp_set_type(req, "text/plain");
  return httpd_resp_send(req, "ok", HTTPD_RESP_USE_STRLEN);
}

// MJPEG stream: one long multipart response, a new JPEG each frame.
static esp_err_t stream_handler(httpd_req_t *req) {
  camera_fb_t *fb = NULL;
  esp_err_t res = httpd_resp_set_type(req, "multipart/x-mixed-replace;boundary=frame");
  if (res != ESP_OK) return res;
  char part[64];
  while (true) {
    fb = esp_camera_fb_get();
    if (!fb) { res = ESP_FAIL; break; }
    size_t hlen = snprintf(part, sizeof(part),
      "--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n", fb->len);
    res = httpd_resp_send_chunk(req, part, hlen);
    if (res == ESP_OK) res = httpd_resp_send_chunk(req, (const char*)fb->buf, fb->len);
    if (res == ESP_OK) res = httpd_resp_send_chunk(req, "\r\n", 2);
    esp_camera_fb_return(fb);
    if (res != ESP_OK) break;   // viewer left - stop streaming to them
  }
  return res;
}

void startServers() {
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port = 80;
  httpd_uri_t page_uri   = { .uri = "/",   .method = HTTP_GET, .handler = page_handler,   .user_ctx = NULL };
  httpd_uri_t go_uri     = { .uri = "/go", .method = HTTP_GET, .handler = go_handler,     .user_ctx = NULL };
  if (httpd_start(&web_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(web_httpd, &page_uri);
    httpd_register_uri_handler(web_httpd, &go_uri);
  }
  httpd_config_t sconfig = HTTPD_DEFAULT_CONFIG();
  sconfig.server_port = 81;
  sconfig.ctrl_port = 32769;
  httpd_uri_t stream_uri = { .uri = "/stream", .method = HTTP_GET, .handler = stream_handler, .user_ctx = NULL };
  if (httpd_start(&stream_httpd, &sconfig) == ESP_OK) {
    httpd_register_uri_handler(stream_httpd, &stream_uri);
  }
}

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  stopCar();

  Serial.begin(115200);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;   config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;   config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;   config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;   config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size   = FRAMESIZE_VGA;    // 640x480 - smooth on soft-AP
  config.jpeg_quality = 12;               // lower number = better quality
  config.fb_count     = psramFound() ? 2 : 1;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init FAILED - check the ribbon cable seating");
    return;
  }

  WiFi.softAP(CAR_WIFI_NAME);
  Serial.print("Network: ");
  Serial.println(CAR_WIFI_NAME);
  Serial.print("Page:    http://");
  Serial.println(WiFi.softAPIP());

  startServers();
}

void loop() {
  delay(10);   // the servers run on their own tasks
}
